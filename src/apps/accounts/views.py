# -*- coding: utf-8 -*-
# python imports
import re
# django imports
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.http import is_safe_url
from django.views.generic import FormView, RedirectView, DetailView, ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# django rest imports
from rest_framework import permissions, renderers, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
# self imports
from .forms import *
from .models import *
from .serializers import *


# ACCOUNTS APP USER CLASSES
# login class view
class LoginView(FormView):
    '''
    Login View
        class based view to enable users to be authenticate
    '''
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('index')
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, allowed_hosts=self.request.get_host()):
            redirect_to = self.success_url
        return redirect_to

    def form_valid(self, form):
        if form.is_valid():
            login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)


# logout class view
class LogoutView(RedirectView):
    '''
    Logout View
        class based view to enable users to clear browser authentication instance
    '''
    url = reverse_lazy('accounts:login')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

        
# user generic class view
class FormUserView(FormView):
    '''
    User View
        class based view for all accounts views to inherit
    '''
    success_url = reverse_lazy('accounts:listUsers')
    template_name = 'common/add.html'
    form_class = UserForm
    model = BasicUser
    page_title = model._meta.verbose_name_plural.title()
    page_subtitle = model._meta.verbose_name.title()
    page_group = "Administrativo"

    def get(self, *args, **kwargs):
        user = self.request.user
        if user.is_active and user.is_admin:
            return super(FormUserView, self).get(*args, **kwargs)
        return HttpResponseRedirect(reverse_lazy('index'))

    def form_valid(self, form):
        # check if user is active
        user = self.request.user
        if user.is_active and user.is_admin:
            
            # save instance
            user = form.save()

            # get logged user
            basic_user = get_object_or_404(BasicUser, pk=self.request.user.id)
            user.created_by = basic_user

            # get avatar field and create new object in database
            avatar_field = form.cleaned_data.get('avatar_field')
            if avatar_field:
                avatar = Avatars.objects.create(avatar = avatar_field)
                user.avatars.add(avatar.id)
            
            # check if user is set to be administrator
            if int(user.profile) == 0:
                user.superuser = True
            else:
                user.superuser = False

            # save object
            user.save()

            return HttpResponseRedirect(self.success_url)

        return super(FormUserView, self).get(form)

    def get_context_data(self, **kwargs):
        context = super(FormUserView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_group'] = self.page_group

        return context


# add user class view
class AddUserView(LoginRequiredMixin, CreateView, FormUserView):
    '''
    Add Project View
        class view to add new users to access the service
    '''
    page_subtitle_action = 'Adicionar'

    def get_context_data(self, **kwargs):
        context = super(AddUserView, self).get_context_data(**kwargs)
        context['page_subtitle'] = f'{self.page_subtitle_action} {self.page_subtitle}'
        return context


# detail user class view
class DetailUserView(LoginRequiredMixin, DetailView):
    '''
    Detail User View
        class base view to detail users
    '''
    template_name = 'accounts/detail_user.html'
    model = BasicUser
    page_title = model._meta.verbose_name_plural.title()
    page_subtitle = model._meta.verbose_name.title()
    page_group = "Administrativo"
    page_subtitle_action = 'Detalhar'

    def get(self, *args, **kwargs):
        user = self.request.user
        if user.is_active and user.is_admin:
            return super(DetailUserView, self).get(*args, **kwargs)
        return HttpResponseRedirect(reverse_lazy('index'))
    
    def get_context_data(self, **kwargs):
        context = super(DetailUserView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = f'{self.page_subtitle_action} {self.page_subtitle}'
        context['page_group'] = self.page_group
        return context


# list users class view
class ListUsersView(LoginRequiredMixin, ListView):
    '''
    List Users View
        class based view to list users with not filter
    '''
    template_name = "accounts/list_users.html"
    page_subtitle_action = 'Listar'
    model = BasicUser
    page_title = model._meta.verbose_name.title()
    page_subtitle = model._meta.verbose_name_plural.title()
    page_group = "Administrativo"
    queryset = BasicUser.objects.filter().order_by('id')
    form = []
    paginate_by = 15

    def get(self, *args, **kwargs):
        user = self.request.user
        if user.is_active and user.is_admin:
            return super(ListUsersView, self).get(*args, **kwargs)
        return HttpResponseRedirect(reverse_lazy('index'))

    def post(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_active:
            return HttpResponseRedirect(reverse_lazy('index'))

        name = self.request.POST['searched_list_name'].upper()

        if name is not '':
            self.queryset = BasicUser.objects.filter(username=name).order_by('id')
        
        return super(ListUsersView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ListUsersView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = f'{self.page_subtitle_action} {self.page_subtitle}'
        context['page_group'] = self.page_group

        return context


# update user class view
class UpdateUserView(LoginRequiredMixin, UpdateView, FormUserView):
    '''
    Update User View
        class based view to update parâmeters from users
    '''
    page_subtitle_action = 'Atualizar'

    def get_context_data(self, **kwargs):
        context = super(UpdateUserView, self).get_context_data(**kwargs)
        context['page_subtitle'] = f'{self.page_subtitle_action} {self.page_subtitle}'

        return context


# delete user class view
class DeleteUserView(LoginRequiredMixin, RedirectView):
    '''
    Delete User View
        class based view to remove user from database
    '''
    model = BasicUser
    url = reverse_lazy('accounts:listUsers')

    def get(self, *args, **kwargs):
        user = self.request.user
        if user.is_active and user.is_admin:
            # 
            basic_user = get_object_or_404(BasicUser, pk=self.kwargs['pk'])
            if not basic_user == user:
                basic_user.delete()

            return super(DeleteUserView, self).get(*args, **kwargs)

        return HttpResponseRedirect(reverse_lazy('index'))


# toggle user active status class view
class ToggleActivationView(LoginRequiredMixin, RedirectView):
    '''
    Toggle Activation View
        class to toggle active status for an existing user in database
    '''
    url = reverse_lazy('accounts:listUsers')

    def get(self, *args, **kwargs):
        user = self.request.user
        if user.is_active and user.is_admin:
            # 
            basic_user = get_object_or_404(BasicUser, pk=kwargs['pk'])
            if not basic_user == self.request.user:
                basic_user.active = not basic_user.active
            basic_user.save()

            return super(ToggleActivationView, self).get(*args, **kwargs)
        
        return HttpResponseRedirect(reverse_lazy('index'))


# toggle user superuser status class view
class ToggleSuperUserView(LoginRequiredMixin, RedirectView):
    '''
    Toggle SuperUser View
        class to toggle superuser status for existing an user in database
    '''
    url = reverse_lazy('accounts:listUsers')

    def get(self, *args, **kwargs):
        user = self.request.user
        if user.is_active and user.is_admin:
            # 
            basic_user = get_object_or_404(BasicUser, pk=kwargs['pk'])
            if not basic_user == self.request.user:
                basic_user.superuser = not basic_user.superuser
                if int(basic_user.profile) == 0:
                    basic_user.profile = get_choices_index(PROFILES, 'Visualização')
            basic_user.save()

            return super(ToggleSuperUserView, self).get(*args, **kwargs)
        
        return HttpResponseRedirect(reverse_lazy('index'))


# update user class view
class UpdateUserPasswordView(LoginRequiredMixin, UpdateView):
    '''
    Update User Passsword View
        class based view to update parâmeters from users
    '''
    success_url = reverse_lazy('accounts:listUsers')
    template_name = 'common/add.html'
    form_class = UpdateUserPasswordForm
    model = BasicUser
    page_title = model._meta.verbose_name_plural.title()
    page_subtitle = model._meta.verbose_name.title()
    page_group = "Administrativo"
    page_subtitle_action = 'Atualizar'

    def get(self, *args, **kwargs):
        # get requested user
        basic_user = get_object_or_404(BasicUser, pk=self.kwargs['pk'])
        # get logged user
        user = self.request.user
        if user.is_active and user.id == basic_user.id:
            return super(UpdateUserPasswordView, self).get(*args, **kwargs)
        return HttpResponseRedirect(reverse_lazy('index'))

    def form_valid(self, form):
        # get requested user
        basic_user = get_object_or_404(BasicUser, pk=self.kwargs['pk'])
        # get logged user
        user = self.request.user
        if user.is_active and user.id == basic_user.id:

            # get form
            user_form = form.save()

            # save object
            user_form.save()

            return HttpResponseRedirect(self.success_url)

        return super(UpdateUserPasswordView, self).get(form)

    def get_context_data(self, **kwargs):
        context = super(UpdateUserPasswordView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = f'{self.page_subtitle_action} {self.page_subtitle}'
        context['page_group'] = self.page_group

        return context
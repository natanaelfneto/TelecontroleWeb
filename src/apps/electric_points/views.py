# -*- coding: utf-8 -*-
# python imports
import datetime
import re
# django imports
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.http import is_safe_url
from django.utils.timezone import utc
from django.views.generic import FormView, RedirectView, DetailView, ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# django rest imports
from rest_framework import permissions, renderers, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
# self imports
from accounts.models import *
from projects.models import *
from .forms import *
from .models import *


# ELECTRIC POINTS CLASSES
# add electric point class view 
class AddElectricPointView(LoginRequiredMixin, CreateView):
    '''
    Add Electric Point View
        class used to add new electric point in database
    '''
    template_name = 'common/add.html'
    model = ElectricPoints
    page_title = model._meta.verbose_name.title()
    page_subtitle = f'Adicionar {model._meta.verbose_name_plural.title()}' 
    page_group = "Administrativo"
    form_class = ElectricPointsForm
    success_url = reverse_lazy('electric_points:listElectricPoints')

    def get(self, *args, **kwargs):
        user = self.request.user
        if ((user.is_active and user.is_admin) or
            (user.is_active and user.is_planner)):

            return super(AddElectricPointView, self).get(*args, **kwargs)

        return HttpResponseRedirect(reverse_lazy('index'))
        

    def form_valid(self, form):
        if self.request.user.is_active:

            # save instance
            electric_point = form.save()

            # get logged user
            basic_user = get_object_or_404(BasicUser, pk = self.request.user.id)
            electric_point.created_by = basic_user

            # create object
            location = Locations.objects.create(
                related_electric_point_name=electric_point.id,
                latitude=form.cleaned_data.get('latitude'),
                longitude=form.cleaned_data.get('longitude'),
                city=form.cleaned_data.get('city'),
                state=form.cleaned_data.get('state'),
                progress_status=get_choices_index(PROGRESS_STATUS, 'A projetar'),
                created_by=basic_user 
            )
            electric_point.locations.add(location.id)

            # save object
            electric_point.save()

            return HttpResponseRedirect(self.success_url)

        return super(AddElectricPointView, self).get(form)

    def get_context_data(self, **kwargs):
        context = super(AddElectricPointView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_group'] = self.page_group

        return context


# detail electric point class
class DetailElectricPointView(LoginRequiredMixin, DetailView):
    '''
    Detail Electric Point View
        class used to show information of electric point from database
    '''
    template_name = 'electric_points/detail_electric_point.html'
    model = ElectricPoints
    page_title = model._meta.verbose_name.title()
    page_subtitle = f'Detalhar {model._meta.verbose_name.title()}' 
    page_group = "Administrativo"
        

# list electric points class
class ListElectricPointsView(LoginRequiredMixin, ListView):
    '''
    List Electric Points View
        class used to list electric points from databased
    '''
    template_name = "electric_points/list_electric_points.html"
    model = ElectricPoints
    page_title = model._meta.verbose_name.title()
    page_subtitle = f'Listar {model._meta.verbose_name_plural.title()}' 
    page_group = "Administrativo"
    queryset = ElectricPoints.objects.filter().order_by('id')
    form = []
    paginate_by = 15

    def post(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_active:
            return HttpResponseRedirect(reverse_lazy('index'))

        name = self.request.POST['searched_list_name']

        if name is not '':
            self.queryset = ElectricPoints.objects.filter(name=name).order_by('id')
        
        return super(ListElectricPointsView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ListElectricPointsView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_group'] = self.page_group

        return context


# update electric point class
class UpdateElectricPointView(LoginRequiredMixin, UpdateView):
    '''
    Update electric Point View
        class used to alter some parameters from existing electric point object in database
    '''
    template_name = 'common/add.html'
    model = ElectricPoints
    page_title = model._meta.verbose_name.title()
    page_subtitle = f'Atualizar {model._meta.verbose_name.title()}' 
    page_group = "Administrativo"
    form_class = ElectricPointsForm
    success_url = reverse_lazy('electric_points:listElectricPoints')

    def get(self, *args, **kwargs):
        user = self.request.user
        if ((user.is_active and user.is_admin) or
            (user.is_active and user.is_planner)):
            
            # check if electric point has a projects associated to it
            if Projects.objects.filter(electric_point=self.kwargs['pk']).distinct():
                return HttpResponseRedirect(reverse_lazy('index'))

            location = Locations.objects.filter(
                electricpoints__id=self.kwargs['pk'],
                obsolete=False
            ).distinct()

            if len(location) > 0:
                self.initial = {
                    'latitude': location[0].latitude,
                    'longitude': location[0].longitude,
                    'city': location[0].city,
                    'state': location[0].state,
                }

            return super(UpdateElectricPointView, self).get(*args, **kwargs)

        return HttpResponseRedirect(reverse_lazy('index'))

    def get_context_data(self, **kwargs):
        context = super(UpdateElectricPointView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_group'] = self.page_group

        return context


# delete electric point class
class DeleteElectricPointView(LoginRequiredMixin, RedirectView):
    '''
    Delete Electric Point View
        class used to remove electric point objects from database
    '''
    model = ElectricPoints
    url = reverse_lazy('electric_points:listElectricPoints')

    def get(self, *args, **kwargs):
        user = self.request.user
        if ((user.is_active and user.is_admin) or
            (user.is_active and user.is_planner)):

            # check if electric point has a projects associated to it
            if Projects.objects.filter(electric_point=self.kwargs['pk']).distinct():
                return HttpResponseRedirect(reverse_lazy('index'))
            
            electric_point = get_object_or_404(ElectricPoints, pk = self.kwargs['pk'])

            # delete all related locations to this electric point
            Locations.objects.filter(electricpoints__id =self.kwargs['pk']).delete()

            electric_point.delete()
            
            return super(DeleteElectricPointView, self).get(*args, **kwargs)

        return HttpResponseRedirect(reverse_lazy('index'))
    

# add project class view
class AddProjectToElectricPointView(LoginRequiredMixin, RedirectView):
    '''
    Add Project To Electric Point View
        class used to add new project object to specific electric point in database
    '''
    model = ElectricPoints
    url = reverse_lazy('electric_points:listElectricPoints')

    def get(self, *args, **kwargs):
        # check if user is active
        user = self.request.user
        if ((user.is_active and user.is_admin) or
            (user.is_active and user.is_designer)):

            # get electric point
            electric_point = get_object_or_404(ElectricPoints, pk=self.kwargs['pk'])

            project = Projects.objects.filter(electric_point=electric_point).distinct()

            if project:
                return HttpResponseRedirect(reverse_lazy('index'))

            # get authenticated user
            basic_user = get_object_or_404(BasicUser, pk = self.request.user.id)

            # create steps for project
            # installation step
            project = Projects.objects.create(
                electric_point=electric_point,
                progress_status=get_choices_index(PROGRESS_STATUS, 'A projetar'),
                created_by=basic_user
            )

            designing = Steps.objects.create(
                project=project,
                progress_status=get_choices_index(PROGRESS_STATUS, 'A projetar')
            )

            designing.save()
            project.designing = designing

            # save object
            project.save()

            # url for successfull progress
            project_id = { 'pk':project.id }
            success_url = reverse_lazy('projects:detailProject', kwargs=project_id)

            return HttpResponseRedirect(success_url)

        return HttpResponseRedirect(reverse_lazy('index'))


# find project for electric point class view
class FindProjectForElectricPointView(LoginRequiredMixin, RedirectView):
    '''
    Find Project For Electric Point View
        class used to show information about existing projects in database
        based on an electric point
    '''
    model = ElectricPoints
    url = reverse_lazy('electric_points:listElectricPoints')

    def get(self, *args, **kwargs):
        user = self.request.user
        if not user.is_active:
            return HttpResponseRedirect(reverse_lazy('index'))

        # get electric point
        electric_point = get_object_or_404(ElectricPoints, pk=self.kwargs['pk']) 

        # get project for specific electric point
        project = get_object_or_404(Projects, electric_point=electric_point)

        # url for successfull progress
        project_id = { 'pk':project.id }
        self.url = reverse_lazy('projects:detailProject', kwargs=project_id)
        
        return HttpResponseRedirect(self.url)


# FEEDERS CLASSES
# add feeder class
class AddFeederView(LoginRequiredMixin, CreateView):
    '''
    Add Fedder View
        class to add new feeder objects in database
    '''
    template_name = 'common/add.html'
    model = Feeders
    page_title = model._meta.verbose_name.title()
    page_subtitle = f'Adicionar {model._meta.verbose_name_plural.title()}' 
    page_group = "Administrativo"
    form_class = FeedersForm
    success_url = reverse_lazy('electric_points:listFeeders')

    def get(self, *args, **kwargs):
        user = self.request.user
        if user.is_active and user.is_admin:
            return super(AddFeederView, self).get(*args, **kwargs)
        return HttpResponseRedirect(reverse_lazy('index'))

    def get_context_data(self, **kwargs):
        context = super(AddFeederView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_group'] = self.page_group

        return context


# detail feeder class
class DetailFeederView(LoginRequiredMixin, DetailView):
    '''
    Detail Feeder View
        class to show information from existing feeder from database
    '''
    template_name = 'feeders/detail_feeders.html'
    model = Feeders
    page_title = model._meta.verbose_name.title()
    page_subtitle = f'Detalhar {model._meta.verbose_name.title()}' 
    page_group = "Administrativo"


# list feeder class
class ListFeedersView(LoginRequiredMixin, ListView):
    '''
    List Feeder View
        class used to list feeder objects from database
    '''
    template_name = "feeders/list_feeders.html"
    model = Feeders
    page_title = model._meta.verbose_name.title()
    page_subtitle = f'Listar {model._meta.verbose_name_plural.title()}' 
    page_group = "Administrativo"
    queryset = Feeders.objects.filter().order_by('id')
    form = []
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super(ListFeedersView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_group'] = self.page_group

        return context


# update feeder class
class UpdateFeederView(LoginRequiredMixin, UpdateView):
    '''
    Update Feeder View
        class used to alter some parameters from existing feeder object in database
    '''
    template_name = 'common/add.html'
    model = Feeders
    page_title = model._meta.verbose_name.title()
    page_subtitle = f'Atualizar {model._meta.verbose_name.title()}' 
    page_group = "Administrativo"
    form_class = FeedersForm
    success_url = reverse_lazy('electric_points:listFeeders')

    def get(self, *args, **kwargs):
        if not self.request.user.is_active or not self.request.user.is_admin:
            return HttpResponseRedirect(reverse_lazy('index'))
        return super(UpdateFeederView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UpdateFeederView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_group'] = self.page_group

        return context


# delete feeder class
class DeleteFeederView(LoginRequiredMixin, RedirectView):
    '''
    Delete Feeder View
        class used to remove feeder objects from database
    '''
    model = Feeders
    url = reverse_lazy('electric_points:listFeeders')

    def get(self, *args, **kwargs):
        if not self.request.user.is_active or not self.request.user.is_admin:
            return HttpResponseRedirect(reverse_lazy('index'))
        
        feeders = get_object_or_404(Feeders, pk = self.kwargs['pk'])
        feeders.delete()

        return super(DeleteFeederView, self).get(*args, **kwargs)

 
# COVERAGE STUDIES CLASSES
# add coverage study class
class AddCoverageStudyView(LoginRequiredMixin, CreateView):
    '''
    Add Coverage Study View
        class to add new coverage study objects in database
    '''
    template_name = 'common/add.html'
    model = CoverageStudies
    page_title = model._meta.verbose_name.title()
    page_subtitle = f'Adicionar {model._meta.verbose_name_plural.title()}' 
    page_group = "Administrativo"
    form_class = StartCoverageStudiesForm
    success_url = reverse_lazy('electric_points:listCoverageStudies')

    def get(self, *args, **kwargs):
        user = self.request.user
        if ((user.is_active and user.is_admin) or
            (user.is_active and user.is_telecom)):

            return super(AddCoverageStudyView, self).get(*args, **kwargs)
        return HttpResponseRedirect(reverse_lazy('index'))

    def form_valid(self, form):
        # check if user is active
        user = self.request.user
        if ((user.is_active and user.is_admin) or
            (user.is_active and user.is_telecom)):
            
            # save instance
            study = form.save()

            project = get_object_or_404(Projects, pk=self.kwargs['pk'])
            study.electric_point = project.electric_point
            study.created_by = user
            study.save()

            project_id = { 'pk':project.id }

            return HttpResponseRedirect(reverse_lazy('projects:detailProject', kwargs=project_id))
        
        return HttpResponseRedirect(reverse_lazy('index'))

    def get_context_data(self, **kwargs):
        context = super(AddCoverageStudyView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_group'] = self.page_group

        return context


# 
class FinishesCoverageStudyView(LoginRequiredMixin, RedirectView):
    '''
    Update Finishe Coverage Study View
        class used to alter some parameters from existing feeder object in database
    '''
    model = CoverageStudies

    def post(self, request, *args, **kwargs):
        # check if user is active
        user = self.request.user
        if ((user.is_active and user.is_admin) or
            (user.is_active and user.is_telecom)):

            study = get_object_or_404(CoverageStudies, pk=self.request.POST['finishes_study_id'])

            study.company_name = self.request.POST['company_name']
            study.mobile_signal = self.request.POST['mobile_signal']
            study.save()

            project = get_object_or_404(Projects, electric_point=study.electric_point)
            project_id = { 'pk':project.id }

            return HttpResponseRedirect(reverse_lazy('projects:detailProject', kwargs=project_id))
        
        return HttpResponseRedirect(reverse_lazy('index'))


# detail coverage study class
class DetailCoverageStudyView(LoginRequiredMixin, DetailView):
    '''
    Detail Feeder View
        class to show information from existing feeder from database
    '''
    template_name = 'feeders/detail_feeders.html'
    model = CoverageStudies
    page_title = model._meta.verbose_name.title()
    page_subtitle = f'Detalhar {model._meta.verbose_name.title()}' 
    page_group = "Administrativo"


# list coverage studies class
class ListCoverageStudiesView(LoginRequiredMixin, ListView):
    '''
    List Feeder View
        class used to list feeder objects from database
    '''
    template_name = "coverage_studies/list_coverage_studies.html"
    model = CoverageStudies
    page_title = model._meta.verbose_name.title()
    page_subtitle = f'Listar {model._meta.verbose_name_plural.title()}' 
    page_group = "Administrativo"
    queryset = CoverageStudies.objects.filter().order_by('id')
    form = []
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super(ListCoverageStudiesView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_group'] = self.page_group

        return context


# delete coverage study class
class DeleteCoverageStudyView(LoginRequiredMixin, RedirectView):
    '''
    Delete Feeder View
        class used to remove feeder objects from database
    '''
    model = CoverageStudies

    def get(self, *args, **kwargs):
        user = self.request.user
        if ((user.is_active or not user.is_admin) or
            (user.is_active or not user.is_telecom)):

            coverage_study = get_object_or_404(CoverageStudies, pk=self.kwargs['pk'])
            coverage_study.delete()

            project = get_object_or_404(Projects, electric_point=coverage_study.electric_point)
            project_id = { 'pk':project.id }

            return HttpResponseRedirect(reverse_lazy('projects:detailProject', kwargs=project_id))
            
        return HttpResponseRedirect(reverse_lazy('index'))
        

# 
class AddSupplyDeliveryView(LoginRequiredMixin, RedirectView):
    '''
    Add Coverage Study View
        class to add new coverage study objects in database
    '''
    model = SupplyDelivery

    def post(self, request, *args, **kwargs):
        # check if user is active
        user = self.request.user
        if ((user.is_active and user.is_admin) or
            (user.is_active and user.is_telecom)):
            
            project = get_object_or_404(Projects, pk=self.kwargs['pk'])

            suppy_delivery = SupplyDelivery.objects.create(
                electric_point=project.electric_point,
                communication_type=self.request.POST['communication_type'],
                equipment_type=self.request.POST['equipment_type'],
                code=self.request.POST['code'],
                serial=self.request.POST['serial'],
                internet_protocol_one=self.request.POST['internet_protocol_one'],
                port_one=self.request.POST['port_one'],
                internet_protocol_two=self.request.POST['internet_protocol_two'],
                port_two=self.request.POST['port_two'],
                created_by=user,
            )
            suppy_delivery.save()

            project_id = { 'pk':project.id }

            return HttpResponseRedirect(reverse_lazy('projects:detailProject', kwargs=project_id))
        
        return HttpResponseRedirect(reverse_lazy('index'))


# list coverage studies class
class ListSupplyDeliveriesView(LoginRequiredMixin, ListView):
    '''
    List  View
        class used to list  objects from database
    '''
    template_name = "supply_deliveries/list_supply_deliveries.html"
    model = SupplyDelivery
    page_title = model._meta.verbose_name.title()
    page_subtitle = f'Listar {model._meta.verbose_name_plural.title()}' 
    page_group = "Administrativo"
    queryset = SupplyDelivery.objects.filter().order_by('id')
    form = []
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super(ListSupplyDeliveriesView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_group'] = self.page_group

        return context


# find project for electric point class view
class FindSupplyDeliveryProjectView(LoginRequiredMixin, RedirectView):
    '''
    Find     View
        class used to show information about existing projects in database
        based on an electric point
    '''
    model = ElectricPoints
    url = reverse_lazy('electric_points:listElectricPoints')

    def get(self, *args, **kwargs):
        user = self.request.user
        if not user.is_active:
            return HttpResponseRedirect(reverse_lazy('index'))

        # get electric point
        supply_delivery = get_object_or_404(SupplyDelivery, pk=self.kwargs['pk']) 

        # get project for specific electric point
        project = get_object_or_404(Projects, electric_point=supply_delivery.electric_point)

        # url for successfull progress
        project_id = { 'pk':project.id }
        self.url = reverse_lazy('projects:detailProject', kwargs=project_id)
        
        return HttpResponseRedirect(self.url)


# find project for electric point class view
class FindCoverageStudyProjectView(LoginRequiredMixin, RedirectView):
    '''
    Find     View
        class used to show information about existing projects in database
        based on an electric point
    '''
    model = ElectricPoints
    url = reverse_lazy('electric_points:listElectricPoints')

    def get(self, *args, **kwargs):
        user = self.request.user
        if not user.is_active:
            return HttpResponseRedirect(reverse_lazy('index'))

        # get electric point
        coverage_study = get_object_or_404(CoverageStudies, pk=self.kwargs['pk']) 

        # get project for specific electric point
        project = get_object_or_404(Projects, electric_point=coverage_study.electric_point)

        # url for successfull progress
        project_id = { 'pk':project.id }
        self.url = reverse_lazy('projects:detailProject', kwargs=project_id)
        
        return HttpResponseRedirect(self.url)


# 
class AddFeederStudyView(LoginRequiredMixin, RedirectView):
    '''
    Add Feeder Study View
        class to add new coverage study objects in database
    '''
    model = FeederStudies

    def post(self, request, *args, **kwargs):
        # check if user is active
        user = self.request.user
        if ((user.is_active and user.is_admin) or
            (user.is_active and user.is_protection)):
            
            project = get_object_or_404(Projects, pk=self.kwargs['pk'])

            feeder_study = FeederStudies.objects.create(
                electric_point=project.electric_point,
                phase_adjustment=self.request.POST['phase_adjustment'],
                neutral_adjustment=self.request.POST['neutral_adjustment'],
                sensitive_neutral_adjustment=self.request.POST['sensitive_neutral_adjustment'],
                shots=self.request.POST['shots'],
                created_by=user,
            )
            feeder_study.save()

            project_id = { 'pk':project.id }

            return HttpResponseRedirect(reverse_lazy('projects:detailProject', kwargs=project_id))
        
        return HttpResponseRedirect(reverse_lazy('index'))


class FinishesFeederStudyView(LoginRequiredMixin, RedirectView):
    '''
    Update  Study View
        class used to alter some parameters from existing feeder object in database
    '''
    model = FeederStudies

    def post(self, request, *args, **kwargs):
        # check if user is active
        user = self.request.user
        if ((user.is_active and user.is_admin) or
            (user.is_active and user.is_protection)):

            feeder_study = get_object_or_404(
                FeederStudies, 
                pk=self.request.POST['finishes_feeder_study_id']
            )

            # get datetime for now
            now = datetime.datetime.utcnow().replace(tzinfo=utc)

            feeder_study.applied_at = now
            feeder_study.applied_by = user
            feeder_study.applied = True
            feeder_study.save()

            project = get_object_or_404(Projects, electric_point=feeder_study.electric_point)
            project_id = { 'pk':project.id }

            return HttpResponseRedirect(reverse_lazy('projects:detailProject', kwargs=project_id))
        
        return HttpResponseRedirect(reverse_lazy('index'))

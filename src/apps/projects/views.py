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
from django.utils.timezone import utc, make_aware
from django.views.generic import FormView, RedirectView, DetailView, ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin
# django rest imports
from rest_framework import permissions, renderers, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
# self imports
from accounts.models import *
from electric_points.forms import *
from electric_points.models import *
from .forms import *
from .models import *


# PROJECTS CLASSES
# add project class view [NOT ACTIVE]
class AddProjectView(LoginRequiredMixin, CreateView):
    '''
    Add Project View
        class used to add new project object in database
    '''
    template_name = 'common/add.html'
    model = Projects
    page_title = model._meta.verbose_name.title()
    page_subtitle = f'Adicionar {model._meta.verbose_name_plural.title()}' 
    page_group = "Administrativo"
    form_class = ProjectsForm
    success_url = reverse_lazy('projects:listProjects')

    def get(self, *args, **kwargs):
        # check if user is active
        user = self.request.user
        if not (user.is_active and user.is_admin) or (user.is_active and user.is_designer):
            return HttpResponseRedirect(reverse_lazy('index'))
        return super(AddProjectView, self).get(*args, **kwargs)

    def form_valid(self, form):
        user = self.request.user
        if ((user.is_active and user.is_admin) or
            (user.is_active and user.is_planner)):

            # save instance
            project = form.save()

            # get authenticated user
            basic_user = get_object_or_404(BasicUser, pk = self.request.user.id)
            project.created_by = basic_user

            # get real date custom field (not naive)
            programmed_date = make_aware(
                datetime.datetime.strptime(self.request.POST['programmed_date'], "%d/%m/%Y")
            )

            # create steps for project
            # installation step
            installation = Steps.objects.create(
                project=project,
                progress_status=get_choices_index(PROGRESS_STATUS, 'A instalar'),
                programmed_date=programmed_date
            )
            installation.save()
            project.installation = installation

            # save object
            project.save()

            return HttpResponseRedirect(self.success_url)

        return HttpResponseRedirect(reverse_lazy('index'))

    def get_context_data(self, **kwargs):
        context = super(AddProjectView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_group'] = self.page_group

        return context


# detail project class view
class DetailProjectView(LoginRequiredMixin, UpdateView):
    '''
    Detail Project View
        class used to show information about existing projects in database
    '''
    template_name = 'projects/detail_project.html'
    model = Projects
    page_title = model._meta.verbose_name.title()
    page_subtitle = f'Movimentar {model._meta.verbose_name.title()}' 
    page_group = "Administrativo"
    fields = []
    form_classes = {
        'pendencies': InstallationPendenciesForm,
        'locations': LocationsForm,
        'project_programmed_date': ProjectProgrammedDateForm,
        'project_real_date': ProjectRealDateForm,
        'coverage_studies_start': StartCoverageStudiesForm,
        'coverage_studies_finishes': FinishesCoverageStudiesForm,
        'telecom_supply_delivery': SupplyDeliveryForm,
        'feeder_study': FeederStudiesForm,
        'sob': ProjectSobForm
    }
    ask_for_programmed_date = None
    success_url = reverse_lazy('projects:listProjects')

    def get(self, *args, **kwargs):
        # set variables runtime initial values
        self.ask_for_programmed_date = {
            'designing': False,
            'installation': False,
            'energizing': False,
            'commissioning': False,
            'operation': False
        }
        self.form_classes['pendencies'] = InstallationPendenciesForm
        self.form_classes['coverage_studies'] = StartCoverageStudiesForm

        # check if user is active
        user = self.request.user
        if not user.is_active:
            return HttpResponseRedirect(reverse_lazy('index'))

        # get project
        project_id = { 'pk':self.kwargs['pk'] }
        project = get_object_or_404(Projects, pk = project_id['pk'])

        location = Locations.objects.filter(
            electricpoints__id=project.electric_point.id,
            obsolete=False
        ).distinct()

        if len(location) > 0:
            self.form_classes['locations'] = LocationsForm(
                initial={
                    'latitude': location[0].latitude,
                    'longitude': location[0].longitude,
                    'city': location[0].city,
                    'state': location[0].state,
                }
            )
        else:
            location = Locations.objects.filter(electricpoints__id=project.electric_point.id).distinct()
            self.form_classes['locations'] = LocationsForm(
                initial={
                    'latitude': location[0].latitude,
                    'longitude': location[0].longitude,
                    'city': location[0].city,
                    'state': location[0].state,
                }
            )

        # check if user is contructor and/or has permissions for energizing
        if ((user.is_active and user.is_admin) or
            (user.is_active and user.is_designer)):

            # check if progress status is designing
            if project.get_progress_status_display() == 'A projetar':
                self.form_classes['pendencies'] = DesigningPendenciesForm

            # check if progress status is energizing and there is not a programmed date for it
            if (project.get_progress_status_display() == 'A projetar' and 
                not project.designing.programmed_date):
                self.ask_for_programmed_date['designing'] = True

        # check if user is contructor and/or has permissions for energizing
        if ((user.is_active and user.is_admin) or
            (user.is_active and user.is_constructor)):

            # check if progress status is installation
            if project.get_progress_status_display() == 'A instalar':
                self.form_classes['pendencies'] = InstallationPendenciesForm

            # check if progress status is energizing and there is not a programmed date for it
            if (project.get_progress_status_display() == 'A instalar' and 
                not project.installation.programmed_date):
                self.ask_for_programmed_date['installation'] = True

            # check if progress status is energizing
            if project.get_progress_status_display() == 'A energizar':
                self.form_classes['pendencies'] = EnergizingPendenciesForm

            # check if progress status is energizing and there is not a programmed date for it
            if (project.get_progress_status_display() == 'A energizar' and 
                not project.energizing.programmed_date):
                self.ask_for_programmed_date['energizing'] = True

        # check if user is telecontrol and/or has permissions for commissioning
        if ((user.is_active and user.is_admin) or
            (user.is_active and user.is_telecontrol)):

            # check if progress status is comissioning
            if project.get_progress_status_display() == 'A comissionar':
                self.form_classes['pendencies'] = CommissioningPendenciesForm

            # check if progress status is comissioning and there is not a programmed date for it
            if (project.get_progress_status_display() == 'A comissionar' and
                not project.commissioning.programmed_date):
                self.ask_for_programmed_date['commissioning'] = True

            # check if progress status is operation
            if project.get_progress_status_display() == 'A operar':
                self.form_classes['pendencies'] = OperationPendenciesForm

            # check if progress status is operation and there is not a programmed date for it
            # while there is a programmed date for commissioning (for redundancy check)
            if (project.get_progress_status_display() == 'A operar' and
                not project.operation.programmed_date and project.commissioning.programmed_date):
                self.ask_for_programmed_date['operation'] = True
        
        return super(DetailProjectView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DetailProjectView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_group'] = self.page_group
        context['forms'] = self.form_classes
        context['ask_for_programmed_date'] = self.ask_for_programmed_date

        return context


# 
class ListProjectsView(LoginRequiredMixin, ListView):
    template_name = "projects/list_projects.html"
    model = Projects
    page_title = model._meta.verbose_name.title()
    page_subtitle = f'Listar {model._meta.verbose_name_plural.title()}' 
    page_group = "Administrativo"
    queryset = Projects.objects.filter().order_by('id')
    form = []
    paginate_by = 15
    electric_regions = Feeders.objects.values('electric_region').distinct()

    def post(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_active:
            return HttpResponseRedirect(reverse_lazy('index'))
        
        progress_status = self.request.POST.get('project_progress_status_filter', False)

        if progress_status and progress_status is not '' and progress_status != "Todos":
            self.queryset = Projects.objects.filter(
                progress_status=get_choices_index(PROGRESS_STATUS, str(progress_status))
            ).order_by('id')

        electric_region = self.request.POST.get('electric_region_filter', False)

        if electric_region and electric_region is not '' and electric_region != "Todas":
            self.queryset = Projects.objects.filter(
                electric_point__feeder__electric_region=electric_region
            ).order_by('id')
        
        return super(ListProjectsView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ListProjectsView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_group'] = self.page_group
        context['electric_regions'] = self.electric_regions

        return context


# 
class UpdateProjectView(LoginRequiredMixin, UpdateView):
    template_name = 'common/add.html'
    model = Projects
    page_title = model._meta.verbose_name.title()
    page_subtitle = f'Atualizar {model._meta.verbose_name.title()}' 
    page_group = "Administrativo"
    form_class = ProjectsForm
    success_url = reverse_lazy('projects:listProjects')

    def get(self, *args, **kwargs):
        # check if user is active
        user = self.request.user
        if not (user.is_active and user.is_admin): # or (user.is_active and user.is_designer):
            return HttpResponseRedirect(reverse_lazy('index'))
        return super(UpdateProjectView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UpdateProjectView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_group'] = self.page_group

        return context


# 
class DeleteProjectView(LoginRequiredMixin, RedirectView):
    model = Projects
    url = reverse_lazy('projects:listProjects')

    def get(self, *args, **kwargs):
        # check if user is active
        user = self.request.user
        if not (user.is_active and user.is_admin) or (user.is_active and user.is_designer):
            return HttpResponseRedirect(reverse_lazy('index'))
        return super(AddProjectView, self).get(*args, **kwargs)

    def get(self, *args, **kwargs):
        if self.request.user.is_active and self.request.user.is_staff:            
            project = get_object_or_404(Projects, pk = self.kwargs['pk'])
            project.delete()

            return super(DeleteProjectView, self).get(*args, **kwargs)

        return super(DeleteProjectView, self).get(*args, **kwargs)


# add pendency class view
class AddPendencyView(LoginRequiredMixin, UpdateView):
    '''
    Add Pendency View
        class to atatch a pendency to a project and downgrade its progress status
    '''
    template_name = 'index.html'
    model = Pendencies
    fields = []

    def post(self, request, *args, **kwargs):
        # default value for registering pendencies is: not allowed
        is_allowed = False

        # check user permissions
        user = self.request.user
        if user.is_active:

            # get project
            project_id = { 'pk':self.kwargs['pk'] }
            project = get_object_or_404(Projects, pk=project_id['pk'])

            # url for successfull progress
            success_url = reverse_lazy('projects:detailProject', kwargs=project_id)
            # url for successfull progress
            no_success_url = reverse_lazy('projects:detailProject', kwargs=project_id)

            # check user permissions # do it for 'designing' status
            if ((user.is_admin or user.is_designer) and
                project.get_progress_status_display() == 'A projetar'):
                # 
                # is_allowed = True
                pass

            # check user permissions # do it for 'installation' status
            if ((user.is_admin or user.is_constructor) and
                project.get_progress_status_display() == 'A instalar'):
                # 
                is_allowed = True

            # check user permissions # do it for 'energizing' status
            if ((user.is_admin or user.is_constructor) and
                project.get_progress_status_display() == 'A energizar'):
                # 
                is_allowed = True

            # check user permissions # do it for 'commissioning' status
            if ((user.is_admin or user.is_telecontrol) and
                project.get_progress_status_display() == 'A comissionar'):
                # 
                is_allowed = True

            # check user permissions # do it for 'operation' status
            if ((user.is_admin or user.is_telecontrol) and
                project.get_progress_status_display() == 'A operar'):
                # 
                is_allowed = True

            # 
            if is_allowed:
                #
                pendency = Pendencies.objects.create(
                    project=project,
                    pendency_type=self.request.POST['pendency_type'],
                    progress_status=project.progress_status,
                    description=self.request.POST['description'],
                    created_by=self.request.user
                )

                # downgrade project progress status
                if not project.get_progress_status_display() == 'A projetar':
                    project.progress_status = str(int(project.progress_status) - 1)

                # 
                project.pendencies.add(pendency.id)

                if project.installation and project.get_progress_status_display() == 'A projetar':
                    step = get_object_or_404(Steps, pk=project.installation.id)
                    project.installation = None
                    project.designing.real_date = None
                    project.designing.save()
                    step.delete()

                if project.energizing and project.get_progress_status_display() == 'A instalar':
                    step = get_object_or_404(Steps, pk=project.energizing.id)
                    project.energizing = None
                    project.installation.real_date = None
                    project.installation.save()
                    step.delete()

                if project.commissioning and project.get_progress_status_display() == 'A energizar':
                    step = get_object_or_404(Steps, pk=project.commissioning.id)
                    project.commissioning = None
                    project.energizing.real_date = None
                    project.energizing.save()
                    step.delete()

                if project.operation and project.get_progress_status_display() == 'A comissionar':
                    step = get_object_or_404(Steps, pk=project.operation.id)
                    project.operation = None
                    project.commissioning.real_date = None
                    project.commissioning.save()
                    step.delete()

                # 
                project.save()

                return HttpResponseRedirect(success_url)
            
            return HttpResponseRedirect(no_success_url)

        return HttpResponseRedirect(reverse_lazy('index'))


# update electric point class view
class UpdateElectricPointView(LoginRequiredMixin, UpdateView):
    '''
    Update Electric Point View
        class used to alter electric point current location parameters
        related to an electric point object in database
    '''
    template_name = 'index.html'
    model = ElectricPoints
    fields = []

    def post(self, request, *args, **kwargs):
        user = self.request.user
        # check user permissions
        if ((user.is_active and user.is_admin) or
            (user.is_active and user.is_designer)):

            # get project
            project_id = { 'pk':self.kwargs['pk'] }
            project = get_object_or_404(Projects, pk=project_id['pk'])

            # set successfull url
            success_url = reverse_lazy('projects:detailProject', kwargs=project_id)

            # authenticated user
            basic_user = get_object_or_404(BasicUser, pk=user.id)

            # update entire queryset of locations related to electric point to an obsolete state
            project.electric_point.locations.filter(
                obsolete=False
            ).update(obsolete=True)

            # create object
            new_location = Locations.objects.create(
                related_electric_point_name=self.request.POST['related_electric_point_name'],
                latitude=self.request.POST['latitude'],
                longitude=self.request.POST['longitude'],
                city=self.request.POST['city'],
                state=self.request.POST['state'],
                created_by=basic_user,
                progress_status=project.progress_status,
                obsolete=False # for redundancy
            )
            new_location.save()

            # relate new location to electric point
            project.electric_point.locations.add(new_location.id)
            project.electric_point.save()

            return HttpResponseRedirect(success_url)

        return HttpResponseRedirect(reverse_lazy('index'))


# update programmed date class view
class UpdateProgrammedDateView(LoginRequiredMixin, UpdateView):
    '''
    Update Programmed Date View
        class used to insert a programmed date for project step object in database
    '''
    template_name = 'index.html'
    model = Projects
    fields = []

    def post(self, request, *args, **kwargs):
        user = self.request.user
        # check user permissions
        if user.is_active:

            # get project
            project_id = { 'pk':self.kwargs['pk'] }
            project = get_object_or_404(Projects, pk = project_id['pk'])

            # get real date custom field (not naive)
            programmed_date = make_aware(
                datetime.datetime.strptime(self.request.POST['programmed_date'], "%d/%m/%Y")
            )

            # get datetime for now
            now = datetime.datetime.utcnow().replace(tzinfo=utc)

            # check if programmed date is in the past
            if (programmed_date.date() - now.date()).days < 0:
                return HttpResponseRedirect(reverse_lazy('index'))

            # url for successfull progress
            success_url = reverse_lazy('projects:detailProject', kwargs=project_id)

            # check user permissions # do it for 'installation' status
            if ((user.is_admin or user.is_designer) and
                project.get_progress_status_display() == 'A projetar'):
                # set programmed date for this projects progress status
                project.designing.programmed_date = programmed_date
                project.designing.save()

            # check user permissions # do it for 'installation' status
            if ((user.is_admin or user.is_constructor) and
                project.get_progress_status_display() == 'A instalar'):
                # set programmed date for this projects progress status
                project.installation.programmed_date = programmed_date
                project.installation.save()

            # check user permissions # do it for 'energizing' status
            if ((user.is_admin or user.is_constructor) and
                project.get_progress_status_display() == 'A energizar'):
                # set programmed date for this projects progress status
                project.energizing.programmed_date = programmed_date
                project.energizing.save()

            # check user permissions # do it for 'commissioning' status
            if ((user.is_admin or user.is_telecontrol) and
                project.get_progress_status_display() == 'A comissionar'):
                # set programmed date for this projects progress status
                project.commissioning.programmed_date = programmed_date
                project.commissioning.save()

            # check user permissions # do it for 'operation' status
            if ((user.is_admin or user.is_telecontrol) and
                project.get_progress_status_display() == 'A operar'):
                # set programmed date for this projects progress status
                project.operation.programmed_date = programmed_date
                project.operation.save()

            # save object
            project.save()

            return HttpResponseRedirect(success_url)

        return HttpResponseRedirect(reverse_lazy('index'))


# update progress status class view
class UpdateProgressStatusView(LoginRequiredMixin, UpdateView):
    '''
    Update Progress Status View
        class to update the project progress status forward and necessary parameters 
    '''
    template_name = 'index.html'
    model = Projects
    fields = []

    def post(self, request, *args, **kwargs):
        user = self.request.user
        # check user permissions
        if ((user.is_active and user.is_admin) or
            (user.is_active and user.is_planner) or
            (user.is_active and user.is_designer) or
            (user.is_active and user.is_constructor) or
            (user.is_active and user.is_telecontrol)):

            # get project
            project_id = { 'pk':self.kwargs['pk'] }
            project = get_object_or_404(Projects, pk = project_id['pk'])

            # get real date custom field (not naive)
            real_date = make_aware(
                datetime.datetime.strptime(self.request.POST['real_date'], "%d/%m/%Y")
            )
            
            # get datetime for now
            now = datetime.datetime.utcnow().replace(tzinfo=utc)

            # check if programmed date is in the past
            if (now.date() - real_date.date()).days < 0:
                return HttpResponseRedirect(reverse_lazy('index'))

            # get pendencies related to this project
            pendencies = Pendencies.objects.filter(
                project=project,
                progress_status=str(int(project.progress_status) + 1),
                solved=False
            ).order_by('id')

            # chech if project has any open pendency and (for redundancy) if it is not finished
            if not pendencies and not project.finished_at:

                # url for successfull progress
                success_url = reverse_lazy('projects:detailProject', kwargs=project_id)

                # check user profile and # do it for 'designing' status
                if ((user.is_admin or user.is_designer) and
                    project.get_progress_status_display() == 'A projetar'):
                    # set real date for this projects progress status

                    if not project.designing.programmed_date:
                        return HttpResponseRedirect(success_url)

                    project.designing.real_date = real_date
                    project.designing.save()

                    # create steps for project
                    # energizing step
                    installation = Steps.objects.create(
                        project=project,
                        progress_status=get_choices_index(PROGRESS_STATUS, 'A instalar'),
                        created_by=user
                    )
                    installation.save()
                    project.installation = installation

                    # upgrade project progress status
                    project.progress_status = str(int(project.progress_status) + 1)

                    # save object
                    project.save()

                    return HttpResponseRedirect(success_url)
                
                # check user profile and # do it for 'installation' status
                if ((user.is_admin or user.is_constructor) and
                    project.get_progress_status_display() == 'A instalar'):
                    # set real date for this projects progress status

                    if not project.designing.programmed_date:
                        return HttpResponseRedirect(success_url)

                    if not project.installation.programmed_date:
                        return HttpResponseRedirect(success_url)

                    project.installation.real_date = real_date
                    project.installation.save()

                    # create steps for project
                    # energizing step
                    energizing = Steps.objects.create(
                        project=project,
                        progress_status=get_choices_index(PROGRESS_STATUS, 'A energizar'),
                        created_by=user
                    )
                    energizing.save()
                    project.energizing = energizing

                    # upgrade project progress status
                    project.progress_status = str(int(project.progress_status) + 1)

                    # save object
                    project.save()

                    return HttpResponseRedirect(success_url)

                # check user profile and # do it for 'energizing' status
                if ((user.is_admin or user.is_constructor) and
                    project.get_progress_status_display() == 'A energizar'):
                    # set real date for this projects progress status

                    if not project.designing.programmed_date:
                        return HttpResponseRedirect(success_url)

                    if not project.installation.programmed_date:
                        return HttpResponseRedirect(success_url)

                    if not project.energizing.programmed_date:
                        return HttpResponseRedirect(success_url)

                    project.energizing.real_date = real_date
                    project.energizing.save()

                    # create steps for project
                    # commissioning step
                    commissioning = Steps.objects.create(
                        project=project,
                        progress_status=get_choices_index(PROGRESS_STATUS, 'A comissionar'),
                        created_by=user
                    )
                    commissioning.save()
                    project.commissioning = commissioning

                    # upgrade project progress status
                    project.progress_status = str(int(project.progress_status) + 1)

                    # save object
                    project.save()

                    return HttpResponseRedirect(success_url)

                # check user profile and # do it for 'commissioning' status
                if ((user.is_admin or user.is_telecontrol) and
                    project.get_progress_status_display() == 'A comissionar'):
                    # set real date for this projects progress status

                    if not project.designing.programmed_date:
                        return HttpResponseRedirect(success_url)

                    if not project.installation.programmed_date:
                        return HttpResponseRedirect(success_url)

                    if not project.energizing.programmed_date:
                        return HttpResponseRedirect(success_url)

                    if not project.commissioning.programmed_date:
                        return HttpResponseRedirect(success_url)

                    project.commissioning.real_date = real_date
                    project.commissioning.save()

                    # create steps for project
                    # operation step
                    operation = Steps.objects.create(
                        project=project,
                        progress_status=get_choices_index(PROGRESS_STATUS, 'A operar'),
                        created_by=user
                    )
                    operation.save()
                    project.operation = operation

                    # upgrade project progress status
                    project.progress_status = str(int(project.progress_status) + 1)

                    # save object
                    project.save()

                    return HttpResponseRedirect(success_url)

                # check user profile and # do it for 'operation' status
                if ((user.is_admin or user.is_telecontrol) and
                    project.get_progress_status_display() == 'A operar'):
                    # set real date for this projects progress status

                    if not project.designing.programmed_date:
                        return HttpResponseRedirect(success_url)

                    if not project.installation.programmed_date:
                        return HttpResponseRedirect(success_url)

                    if not project.energizing.programmed_date:
                        return HttpResponseRedirect(success_url)

                    if not project.commissioning.programmed_date:
                        return HttpResponseRedirect(success_url)

                    if not project.operation.programmed_date:
                        return HttpResponseRedirect(success_url)

                    project.operation.real_date = real_date
                    project.operation.save()

                    # set project finished date to datetime of now
                    project.finished_at = now
                    project.finished_by = user

                    # upgrade project progress status
                    project.progress_status = str(int(project.progress_status) + 1)

                    # save object
                    project.save()

                    return HttpResponseRedirect(success_url)
                
                return HttpResponseRedirect(success_url)
                
            # if project has pendencies
            elif pendencies:
                # url for unsuccessfull progress
                no_success_url = reverse_lazy('projects:unsolvedPendencies', kwargs=project_id)

            return HttpResponseRedirect(no_success_url)

        return HttpResponseRedirect(reverse_lazy('index'))


# 
class UnsolvedPendenciesView(LoginRequiredMixin, TemplateView):
    '''
    '''
    template_name = "projects/unsolved-pendencies.html"
    model = Projects
    page_title = model._meta.verbose_name.title()
    page_subtitle = f'Erro de Movimentação de {model._meta.verbose_name.title()}' 
    page_group = "Administrativo"

    def get_context_data(self, **kwargs):
        context = super(UnsolvedPendenciesView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_group'] = self.page_group
        context['project'] = get_object_or_404(Projects, pk = self.kwargs['pk'])

        return context


#  solve pendency class view
class SolvePendencyView(LoginRequiredMixin, RedirectView):
    '''
    Solve Pendency View
        class to set existing pendencies as solved in database
    '''
    model = Pendencies
    url = reverse_lazy('index')

    def get(self, *args, **kwargs):
        # default value for registering pendencies is: not allowed
        is_allowed = False

        # get datetime for now
        now = datetime.datetime.utcnow().replace(tzinfo=utc)

        # check user permissions
        user = self.request.user
        if user.is_active:

            # get pendency
            pendency_id = { 'pk':self.kwargs['pendency_pk'] }
            pendency = get_object_or_404(Pendencies, pk = pendency_id['pk'])

            # get project
            project_id = { 'pk':pendency.project.id }

            # url for successfull progress
            success_url = reverse_lazy('projects:detailProject', kwargs=project_id)
            # url for successfull progress
            no_success_url = reverse_lazy('projects:detailProject', kwargs=project_id)

            # check user permissions # do it for 'installation' status
            if ((user.is_admin or user.is_designer) and
                pendency.get_progress_status_display() == 'A instalar'):
                # 
                is_allowed = True

            # check user permissions # do it for 'installation' status
            if ((user.is_admin or user.is_planner) and
                pendency.get_progress_status_display() == 'A energizar'):
                # 
                is_allowed = True

            # check user permissions # do it for 'energizing' status
            if ((user.is_admin or user.is_constructor) and
                pendency.get_progress_status_display() == 'A comissionar'):
                # 
                is_allowed = True

            # check user permissions # do it for 'commissioning' status
            if ((user.is_admin or user.is_telecontrol) and
                pendency.get_progress_status_display() == 'A operar'):
                # 
                is_allowed = True

            # 
            if is_allowed:

                # set pendency as solved
                pendency.solved = True
                pendency.solved_at = now

                # save object
                pendency.save()

                return HttpResponseRedirect(success_url)
            
            return HttpResponseRedirect(no_success_url)

        return HttpResponseRedirect(reverse_lazy('index'))


class AddProjectSOBView(LoginRequiredMixin, UpdateView):
    template_name = 'index.html'
    model = Projects
    fields = []

    def post(self, request, *args, **kwargs):

        # check user permissions
        user = self.request.user
        if user.is_active:

            # get project
            project_id = { 'pk':self.kwargs['pk'] }
            project = get_object_or_404(Projects, pk=project_id['pk'])

            # url for successfull progress
            success_url = reverse_lazy('projects:detailProject', kwargs=project_id)
            # url for successfull progress
            no_success_url = reverse_lazy('projects:detailProject', kwargs=project_id)

            # check user permissions # do it for 'energizing' status
            if user.is_admin or user.is_constructor:
                # 
                project.sob = self.request.POST['sob']
                print(project.sob)
                project.save()

                return HttpResponseRedirect(success_url)
            
            return HttpResponseRedirect(no_success_url)

        return HttpResponseRedirect(reverse_lazy('index'))
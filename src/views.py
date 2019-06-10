# -*- coding: utf-8 -*-
# django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.base import TemplateView
# 
from accounts.models import *
from electric_points.models import *
from projects.models import *

# 
class IndexView(LoginRequiredMixin, TemplateView):
    '''
    '''
    template_name = "index.html"
    page_title = "Visão Geral"
    page_subtitle = "Dashboard"
    page_group = "Acompanhamento"
    models = {}

    def get(self, *args, **kwargs):
        # check if user is active
        user = self.request.user
        if not user.is_active:
            return HttpResponseRedirect(reverse_lazy('index'))

        self.models = {
            'electric_points': {
                'total': ElectricPoints.objects.all().count(),
                'designing': Projects.objects.filter(
                        step_project__progress_status=get_choices_index(PROGRESS_STATUS, 'A projetar'),
                    ).count(),
                'installation': Projects.objects.filter(
                        step_project__progress_status=get_choices_index(PROGRESS_STATUS, 'A instalar')
                    ).count(),
                'energizing': Projects.objects.filter(
                        step_project__progress_status=get_choices_index(PROGRESS_STATUS, 'A energizar')
                    ).count(),
                'commissioning': Projects.objects.filter(
                        step_project__progress_status=get_choices_index(PROGRESS_STATUS, 'A comissionar')
                    ).count(),
                'operation': Projects.objects.filter(
                        step_project__progress_status=get_choices_index(PROGRESS_STATUS, 'A operar')
                    ).count(),
                'finished': Projects.objects.filter(
                        step_project__progress_status=get_choices_index(PROGRESS_STATUS, 'Concluído')
                    ).count(),
            },
            'projects': {
                'total': Projects.objects.all().count(),
                'designing': Projects.objects.filter(
                        progress_status=get_choices_index(PROGRESS_STATUS, 'A projetar')
                    ).count(),
                'installation': Projects.objects.filter(
                        progress_status=get_choices_index(PROGRESS_STATUS, 'A instalar')
                    ).count(),
                'energizing': Projects.objects.filter(
                        progress_status=get_choices_index(PROGRESS_STATUS, 'A energizar')
                    ).count(),
                'commissioning': Projects.objects.filter(
                        progress_status=get_choices_index(PROGRESS_STATUS, 'A comissionar')
                    ).count(),
                'operation': Projects.objects.filter(
                        progress_status=get_choices_index(PROGRESS_STATUS, 'A operar')
                    ).count(),
                'finished': Projects.objects.filter(
                        progress_status=get_choices_index(PROGRESS_STATUS, 'Concluído')
                    ).count(),
            },
            'pendencies': {
                'total': Projects.objects.all().count(),
                'designing': Projects.objects.filter(
                        progress_status=get_choices_index(PROGRESS_STATUS, 'A projetar'),
                    ).exclude(
                        pendencies=None
                    ).count(),
                'installation': Projects.objects.filter(
                        progress_status=get_choices_index(PROGRESS_STATUS, 'A instalar')
                    ).exclude(
                        pendencies=None
                    ).count(),
                'energizing': Projects.objects.filter(
                        progress_status=get_choices_index(PROGRESS_STATUS, 'A energizar')
                    ).exclude(
                        pendencies=None
                    ).count(),
                'commissioning': Projects.objects.filter(
                        progress_status=get_choices_index(PROGRESS_STATUS, 'A comissionar')
                    ).exclude(
                        pendencies=None
                    ).count(),
                'operation': Projects.objects.filter(
                        progress_status=get_choices_index(PROGRESS_STATUS, 'A operar')
                    ).exclude(
                        pendencies=None
                    ).count(),
                'finished': Projects.objects.filter(
                        progress_status=get_choices_index(PROGRESS_STATUS, 'Concluído')
                    ).exclude(
                        pendencies=None
                    ).count(),
            },
            'feeders': {
                'electric_regions': {
                    'names': Feeders.objects.values('electric_region').distinct(),
                    'count': {},
                },
            },
        }

        for progress_status in PROGRESS_STATUS:
            self.models['feeders']['electric_regions']['count'][progress_status[1]] = {}
            for name in self.models['feeders']['electric_regions']['names']:
                electric_region_count = Projects.objects.filter(
                    electric_point__feeder__electric_region=name['electric_region'],
                    progress_status=progress_status[0]
                ).count()
                self.models['feeders']['electric_regions']['count'][progress_status[1]][name['electric_region']] = electric_region_count

        return super(IndexView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_group'] = self.page_group
        context['models'] = self.models

        return context


#
class HandlerView():        

    def handler404(request, exception):
        context = {
            'error': '404',
            'error_description': 'Desculpe, mas a página solicitada não foi encontrada'
        }
        return render(request, 'common/error.html', context)

    def handler500(request):
        context = {
            'error': '500',
            'error_description': 'Desculpe, uma instabilidade no servidor impediu \
                que a página solicitada fosse carregada'
        }
        return render(request, 'common/error.html', context)
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
                'year_2019': {
                    'total':''
                },
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
                'year_2019': {
                    'total':'',
                    'installation_0':Projects.objects.filter(
                        progress_status=get_choices_index(PROGRESS_STATUS, 'A projetar'),
                        pendencies__pendency_type=str(get_choices_index(
                            PENDENCIES_TYPES['installation'],
                            'Materiais de Obras'
                    ))).count(),
                    'energizing_0':Projects.objects.filter(
                        progress_status=get_choices_index(PROGRESS_STATUS, 'A instalar'),
                        pendencies__pendency_type=str(get_choices_index(
                            PENDENCIES_TYPES['energizing'],
                            'Obra não concluída'
                    ))).count(),
                    'commissioning_0':Projects.objects.filter(
                        progress_status=get_choices_index(PROGRESS_STATUS, 'A energizar'),
                        pendencies__pendency_type=str(get_choices_index(
                            PENDENCIES_TYPES['commissioning'],
                            'Cobertura não condiz com estudo teórico'
                    ))).count(),
                    'commissioning_1':Projects.objects.filter(
                        progress_status=get_choices_index(PROGRESS_STATUS, 'A energizar'),
                        pendencies__pendency_type=str(get_choices_index(
                            PENDENCIES_TYPES['commissioning'],
                            'Equipamento de Telecom com defeito'
                    ))).count(),
                    'commissioning_2':Projects.objects.filter(
                        progress_status=get_choices_index(PROGRESS_STATUS, 'A energizar'),
                        pendencies__pendency_type=str(get_choices_index(
                            PENDENCIES_TYPES['commissioning'],
                            'Equipamento de Telecom com defeito'
                    ))).count(),
                    'commissioning_3':Projects.objects.filter(
                        progress_status=get_choices_index(PROGRESS_STATUS, 'A energizar'),
                        pendencies__pendency_type=str(get_choices_index(
                            PENDENCIES_TYPES['commissioning'],
                            'Falta conectar MT'
                    ))).count(),
                    'commissioning_4':Projects.objects.filter(
                        progress_status=get_choices_index(PROGRESS_STATUS, 'A energizar'),
                        pendencies__pendency_type=str(get_choices_index(
                            PENDENCIES_TYPES['commissioning'],
                            'IMS sem bateria'
                    ))).count(),
                    'commissioning_5':Projects.objects.filter(
                        progress_status=get_choices_index(PROGRESS_STATUS, 'A energizar'),
                        pendencies__pendency_type=str(get_choices_index(
                            PENDENCIES_TYPES['commissioning'],
                            'Sem cadastro no mapa'
                    ))).count(),
                    'commissioning_6':Projects.objects.filter(
                        progress_status=get_choices_index(PROGRESS_STATUS, 'A energizar'),
                        pendencies__pendency_type=str(get_choices_index(
                            PENDENCIES_TYPES['commissioning'],
                            'Tensão TP inadequada'
                    ))).count(),
                    'operation_0':Projects.objects.filter(
                        progress_status=get_choices_index(PROGRESS_STATUS, 'A comissionar'),
                        pendencies__pendency_type=str(get_choices_index(
                            PENDENCIES_TYPES['operation'],
                            'Padrão'
                    ))).count(),
                }
            },
            'feeders': {
                'electric_regions': {
                    'names': Feeders.objects.values('electric_region').distinct(),
                    'count': {},
                },
            },
        }

        print(Projects.objects.filter(pendencies__pendency_type='5').values('progress_status'))
        print(self.models['pendencies']['year_2019'])

        for progress_status in PROGRESS_STATUS:
            if not progress_status[1] == 'Concluído':
                for month in range(1,13):

                    project_count = Projects.objects.filter(
                        step_project__progress_status=progress_status[0],
                        step_project__real_date__year=2019,
                        step_project__real_date__month=month,
                    ).count(),
                    
                    if not str(PROGRESS_STATUS[int(progress_status[0]) + 1][1]) in self.models['projects']['year_2019']:
                        self.models['projects']['year_2019'][str(PROGRESS_STATUS[int(progress_status[0]) + 1][1])] = {}
                    
                    self.models['projects']['year_2019'][str(PROGRESS_STATUS[int(progress_status[0]) + 1][1])][f'month_{str(month)}'] = project_count
            else:
                for month in range(1,13):

                    project_count = Projects.objects.filter(
                        progress_status=progress_status[0],
                        finished_at__year=2019,
                        finished_at__month=month,
                    ).count(),
                    
                    if not progress_status[1] in self.models['projects']['year_2019']:
                        self.models['projects']['year_2019'][progress_status[1]] = {}

                    self.models['projects']['year_2019'][progress_status[1]][f'month_{str(month)}'] = project_count

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
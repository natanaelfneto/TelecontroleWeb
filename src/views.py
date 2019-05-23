# -*- coding: utf-8 -*-
# django imports
from django.contrib.auth.mixins import LoginRequiredMixin
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
    models = {
        'electric_points': {
            'total': ElectricPoints.objects.all().count(),
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
        }
    }

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_group'] = self.page_group
        context['models'] = self.models

        return context
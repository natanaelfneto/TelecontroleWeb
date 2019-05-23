# -*- coding: utf-8 -*-
# django imports
from django import template
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import stringfilter
# self imports
from electric_points.models import SupplyDelivery
from ..models import *


# 
register = template.Library()

# 
@register.filter(name='get_electric_point_name')
def get_electric_point_name(electric_point_id):
    #
    electric_point = ElectricPoints.objects.filter(
        pk=int(electric_point_id)
    )
    if len(electric_point) > 0:
        return electric_point[0].name
    
    return "Removido por Planejamento"
    
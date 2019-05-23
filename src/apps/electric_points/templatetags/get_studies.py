# -*- coding: utf-8 -*-
# django imports
from django import template
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import stringfilter
# self imports
from electric_points.models import CoverageStudies
from ..models import *


# 
register = template.Library()

# 
@register.filter(name='get_studies')
def get_studies(electric_point, arg):
    # 
    if str(arg) == 'coverage_studies':
        return CoverageStudies.objects.filter(electric_point=electric_point)
    
    elif str(arg) == 'feeder_studies':
        return FeederStudies.objects.filter(electric_point=electric_point)
    
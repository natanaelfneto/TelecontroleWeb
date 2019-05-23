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
@register.filter(name='get_supplies')
def get_supplies(electric_point):
    # 
    return SupplyDelivery.objects.filter(electric_point=electric_point)
    
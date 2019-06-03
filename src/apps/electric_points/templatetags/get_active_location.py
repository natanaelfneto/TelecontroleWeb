# -*- coding: utf-8 -*-
# django imports
from django import template
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import stringfilter
# self imports
from ..models import *


# 
register = template.Library()

# 
@register.filter(name='get_active_location')
def get_active_location(received_object, arg):
    # 
    try:
        electric_point = ElectricPoints.objects.get(pk=int(received_object))
        last_active_location = electric_point.locations.order_by('-created_at')[0]        
        electric_point_name = electric_point.name
    except:
        last_active_location = received_object.order_by('-created_at')[0]
        pass

    if str(arg) == 'related_electric_point_name':
        return last_active_location.related_electric_point_name
    # 
    if str(arg) == 'latitude':
        return last_active_location.latitude

    elif str(arg) == 'longitude':
        return last_active_location.longitude

    elif str(arg) == 'city':
        return last_active_location.city

    elif str(arg) == 'get_city_display':
        return last_active_location.get_city_display()

    elif str(arg) == 'state':
        return last_active_location.state

    elif str(arg) == 'get_state_display':
        return last_active_location.get_state_display()

    else:
        return None

    
        
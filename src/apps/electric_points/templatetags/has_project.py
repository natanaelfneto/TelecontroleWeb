# -*- coding: utf-8 -*-
# django imports
from django import template
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import stringfilter
# self imports
from projects.models import Projects
from ..models import *


# 
register = template.Library()

# 
@register.filter(name='has_project')
def has_project(electric_point):
    # 
    if Projects.objects.filter(electric_point=electric_point).distinct():
        return True
    
    return False

    
        
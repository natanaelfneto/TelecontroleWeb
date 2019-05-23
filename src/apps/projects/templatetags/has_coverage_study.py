# -*- coding: utf-8 -*-
# django imports
from django import template
# 
from electric_points.models import CoverageStudies

# 
register = template.Library()

#
@register.filter(name='has_coverage_study')
def has_coverage_study(project):
    # 
    if not CoverageStudies.objects.filter(electric_points=project.electric_point):
        return True

    return False
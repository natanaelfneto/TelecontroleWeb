# -*- coding: utf-8 -*-
# django imports
from django import template
# 
from ..models import Pendencies

# 
register = template.Library()

#
@register.filter(name='has_pendencies')
def has_pendencies(project):
    if Pendencies.objects.filter(
        project=project, 
        progress_status=str(int(project.progress_status) + 1), 
        solved=False).order_by('id'):
        # 
        return True

    return False
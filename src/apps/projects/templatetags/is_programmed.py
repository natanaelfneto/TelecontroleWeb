# -*- coding: utf-8 -*-
# django imports
from django import template


# 
register = template.Library()

#
@register.filter(name='is_programmed')
def is_programmed(project):

    if project.designing and project.designing.programmed_date is None:
        return False
    
    if project.installation and project.installation.programmed_date is None:
        return False

    if project.energizing and project.energizing.programmed_date is None:
        return False
    
    if project.commissioning and project.commissioning.programmed_date is None:
        return False

    if project.operation and project.operation.programmed_date is None:
        return False

    return True
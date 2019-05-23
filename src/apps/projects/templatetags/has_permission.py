# -*- coding: utf-8 -*-
# django imports
from django import template


# 
register = template.Library()

#
@register.filter(name='has_permission')
def has_permission(profile, progress_status):

    # 
    if profile == 'Administração':
        return True

    if progress_status == 'A projetar' and profile == 'Projeto':
        return True

    # 
    if progress_status == 'A instalar' and profile == 'Obras':
        return True

    # 
    if progress_status == 'A energizar' and profile == 'Obras':
        return True

    # 
    if progress_status == 'A comissionar' and profile == 'Telecontrole':
        return True

    # 
    if progress_status == 'A operar' and profile == 'Telecontrole':
        return True

    return False
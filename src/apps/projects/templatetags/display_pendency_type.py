# -*- coding: utf-8 -*-
# django imports
from django import template
# 
from accounts.models import get_choices_index
from ..models import PENDENCIES_TYPES

# 
register = template.Library()

#
@register.filter(name='display_pendency_type')
def display_pendency_type(pendency, arg):
 
    if str(arg) == 'type':

        if pendency.get_progress_status_display() == 'A projetar':
            return None

        if pendency.get_progress_status_display() == 'A instalar':
            return dict(PENDENCIES_TYPES['installation'])[pendency.pendency_type]

        if pendency.get_progress_status_display() == 'A energizar':
            return dict(PENDENCIES_TYPES['energizing'])[pendency.pendency_type]

        if pendency.get_progress_status_display() == 'A comissionar':
            return dict(PENDENCIES_TYPES['commissioning'])[pendency.pendency_type]

        if pendency.get_progress_status_display() == 'A operar':
            return dict(PENDENCIES_TYPES['operation'])[pendency.pendency_type]

    elif str(arg) == 'responsable':

        if pendency.get_progress_status_display() == 'A projetar':
            return 'Projeto'

        if pendency.get_progress_status_display() == 'A instalar':
            return 'Obras'

        if pendency.get_progress_status_display() == 'A energizar':
            return 'Obras'

        if pendency.get_progress_status_display() == 'A comissionar':
            return 'Telecontrole'

        if pendency.get_progress_status_display() == 'A operar':
            return 'Telecontrole'

    return None
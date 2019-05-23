# -*- coding: utf-8 -*-
# django imports
from django import template
# 
from accounts.models import get_choices_index
from ..models import COVERAGE_STUDIES_COMMUNICATION_TYPES

# 
register = template.Library()

#
@register.filter(name='display_coverage_studies_type')
def display_coverage_studies_type(study, arg):
 
    if str(arg) == 'type':
        return dict(COVERAGE_STUDIES_COMMUNICATION_TYPES['0'])[study.communication_type]

    return None
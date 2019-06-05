# -*- coding: utf-8 -*-
# django imports
from django import template
# 
from ..models import Pendencies

# 
register = template.Library()

#
@register.filter(name='decimal_filter')
def decimal_filter(value):
    return f'{float(value):.1f}'
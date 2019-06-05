# -*- coding: utf-8 -*-
# django imports
from django import template
# 
from ..models import Pendencies

# 
register = template.Library()

#
@register.filter(name='div_by_zero')
def div_by_zero(numerator, denominator):
    return f'{numerator / denominator if denominator else 0}'
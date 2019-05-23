# -*- coding: utf-8 -*-
# django imports
from django import template
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import stringfilter
# self imports
from ..models import Avatars, BasicUser


# 
register = template.Library()

# 
@register.filter(name='get_most_recent_avatar_url')
def get_most_recent_avatar_url(user_id):    
    # get basic user
    basic_user = get_object_or_404(BasicUser, pk=user_id)

    # check if length of avatar many to many list is different than zero
    if len(list(basic_user.avatars.all())) != 0:

        # return first avatar url on database ordered by its upload time
        return basic_user.avatars.order_by('uploaded_at')[0].avatar.url
        
    # if not avatar is found for user, return default avatar image url
    return static('img/avatars/default.jpg')
    

# -*- coding: utf-8 -*-
# django imports
from django.contrib import admin
# self imports
from .models import *


# register BasicUser class to Admin
admin.site.register(BasicUser)
admin.site.register(Avatars)

# -*- coding: utf-8 -*-
# django imports
from django.contrib import admin
# self imports
from .models import *


# register BasicUser class to Admin
admin.site.register(ElectricPoints)
admin.site.register(Feeders)
admin.site.register(Locations)
admin.site.register(CoverageStudies)
admin.site.register(SupplyDelivery)
admin.site.register(FeederStudies)
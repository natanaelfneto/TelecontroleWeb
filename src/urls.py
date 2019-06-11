# -*- coding: utf-8 -*-
# django imports
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
# self imports
from .views import *

# 
urlpatterns = [
    # index url
    url(r'^$', IndexView.as_view(), name='index'),

    # app accounts urls
    url(r'^accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),

    # app accounts urls
    url(r'^electric_points/', include(('electric_points.urls', 'electric_points'), namespace='electric_points')),

    # app accounts urls
    url(r'^projects/', include(('projects.urls', 'projects'), namespace='projects')),

    # admin urls
    path('admin/', admin.site.urls),
]

handler404 = HandlerView.handler404
handler500 = HandlerView.handler500

# 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# -*- coding: utf-8 -*-
# django imports
from django.conf.urls import url
# self imports
from .views import *


# 
urlpatterns = [

    # Electric Points
    # add new user page
    # url(r'add/$', AddProjectView.as_view(), name='addProject'),
    # detail information of user page
    url(r'(?P<pk>\d+)/detail/$', DetailProjectView.as_view(), name='detailProject'),
    # detail information of user page
    url(r'(?P<pk>\d+)/update/$', UpdateProjectView.as_view(), name='updateProject'),
    # detail information of user page
    url(r'(?P<pk>\d+)/delete/$', DeleteProjectView.as_view(), name='deleteProject'),
    # 
    url(r'(?P<pk>\d+)/update-programmed_date/$', UpdateProgrammedDateView.as_view(), name='updateProgrammedDate'),
    # 
    url(r'(?P<pk>\d+)/update-progress-status/$', UpdateProgressStatusView.as_view(), name='updateProgressStatus'),
    # 
    url(r'(?P<pk>\d+)/pendencies/$', AddPendencyView.as_view(), name='addPendency'),
    # 
    url(r'(?P<pk>\d+)/unsolved-pendencies/$', UnsolvedPendenciesView.as_view(), name='unsolvedPendencies'),
    # 
    url(r'(?P<pendency_pk>\d+)/solve-pendency/$', SolvePendencyView.as_view(), name='solvePendency'),
    # 
    url(r'(?P<pk>\d+)/update-electric-point/$', UpdateElectricPointView.as_view(), name='updateElectricPoint'),
    # 
    url(r'(?P<pk>\d+)/add-sob/$', AddProjectSOBView.as_view(), name='addProjectSOB'),
    # 
    url(r'$', ListProjectsView.as_view(), name='listProjects'),

]
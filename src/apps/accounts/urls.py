# -*- coding: utf-8 -*-
# django imports
from django.conf.urls import url
# self imports
from .views import *


# 
urlpatterns = [
    # login page
    url(r'login/$', LoginView.as_view(), name='login'),

    # logout page
    url(r'logout/$', LogoutView.as_view(), name='logout'),

    # add new user page
    url(r'users/add/$', AddUserView.as_view(), name='addUser'),

    # detail information of user page
    url(r'users/(?P<pk>\d+)/detail/$', DetailUserView.as_view(), name='detailUser'),

    # list all users page
    url(r'users/$', ListUsersView.as_view(), name='listUsers'),

    # update information of user page
    url(r'users/(?P<pk>\d+)/update/$', UpdateUserView.as_view(), name='updateUser'),

    # remove information of user page
    url(r'users/(?P<pk>\d+)/delete/$', DeleteUserView.as_view(), name='deleteUser'),

    # toggle activation flag of user page
    url(r'users/(?P<pk>\d+)/toggle-activation/$', ToggleActivationView.as_view(), name='toggleActivation'),

    # toggle superuser flag of user page
    url(r'users/(?P<pk>\d+)/toggle-superuser/$', ToggleSuperUserView.as_view(), name='toggleSuperUser'),
]
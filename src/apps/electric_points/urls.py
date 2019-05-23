# -*- coding: utf-8 -*-
# django imports
from django.conf.urls import url
# self imports
from .views import *


# 
urlpatterns = [

    # Electric Points
    # add new user page
    url(r'electric_points/add/$', AddElectricPointView.as_view(), name='addElectricPoint'),
    # detail information of user page
    url(r'electric_points/(?P<pk>\d+)/detail/$', DetailElectricPointView.as_view(), name='detailElectricPoint'),
    # detail information of user page
    url(r'electric_points/(?P<pk>\d+)/update/$', UpdateElectricPointView.as_view(), name='updateElectricPoint'),
    # detail information of user page
    url(r'electric_points/(?P<pk>\d+)/delete/$', DeleteElectricPointView.as_view(), name='deleteElectricPoint'),
    # list all users page
    url(r'electric_points/$', ListElectricPointsView.as_view(), name='listElectricPoints'),
    # add project to specific electric point
    url(r'(?P<pk>\d+)/add-project-to-electric-point/$', AddProjectToElectricPointView.as_view(), name='addProjectToElectricPoint'),
    # 
    url(r'(?P<pk>\d+)/find-project-to-electric-point/$', FindProjectForElectricPointView.as_view(), name='findProjectForElectricPoint'),

    # Feeders
    # add new feeder page
    url(r'feeders/add/$', AddFeederView.as_view(), name='addFeeder'),
    # detail information of feeder page
    url(r'feeders/(?P<pk>\d+)/detail/$', DetailFeederView.as_view(), name='detailFeeder'),
    # detail information of feeder page
    url(r'feeders/(?P<pk>\d+)/update/$', UpdateFeederView.as_view(), name='updateFeeder'),
    # detail information of feeder page
    url(r'feeders/(?P<pk>\d+)/delete/$', DeleteFeederView.as_view(), name='deleteFeeder'),
    # list all feeders page
    url(r'feeders/$', ListFeedersView.as_view(), name='listFeeders'),

    # Coverage Studies
    # add new coverage study page
    url(r'coverage-studies/(?P<pk>\d+)/add/$', AddCoverageStudyView.as_view(), name='addCoverageStudy'),
    # 
    url(r'coverage-studies/(?P<pk>\d+)/finishes/$', FinishesCoverageStudyView.as_view(), name='finishesCoverageStudy'),
    # detail information of coverage study page
    url(r'coverage-studies/(?P<pk>\d+)/detail/$', DetailCoverageStudyView.as_view(), name='detailCoverageStudy'),
    # detail information of coverage study page
    # url(r'coverage-studies/(?P<pk>\d+)/update/$', UpdateCoverageStudyView.as_view(), name='updateCoverageStudy'),
    # detail information of coverage study page
    url(r'coverage-studies/(?P<pk>\d+)/delete/$', DeleteCoverageStudyView.as_view(), name='deleteCoverageStudy'),
    # 
    url(r'(?P<pk>\d+)/find-coverage-study-project/$', FindCoverageStudyProjectView.as_view(), name='findCoverageStudyProject'),
    # list all coverage studies page
    url(r'coverage-studies/$', ListCoverageStudiesView.as_view(), name='listCoverageStudies'),

    # 
    # 
    url(r'supply-deliveries/(?P<pk>\d+)/add/$', AddSupplyDeliveryView.as_view(), name='addSupplyDelivery'),
    # 
    url(r'supply-deliveries/$', ListSupplyDeliveriesView.as_view(), name='listSupplyDeliveries'),
    # 
    url(r'(?P<pk>\d+)/find-supply-delivery-project/$', FindSupplyDeliveryProjectView.as_view(), name='findSupplyDeliveryProject'),

    # 
    # 
    url(r'feeder-studies/(?P<pk>\d+)/add/$', AddFeederStudyView.as_view(), name='addFeederStudy'),
    # 
    url(r'feeder-studies/(?P<pk>\d+)/finishes/$', FinishesFeederStudyView.as_view(), name='finishesFeederStudy'),
]
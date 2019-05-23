# -*- coding: utf-8 -*-
# python imports
import random
import re
# django imports
from django.conf import settings
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models
# self imports
from projects.models import PROGRESS_STATUS
from .brazil_goias_cities import *


EQUIPMENT_TYPE = (
    ('0', 'Chave'),
    ('1', 'Religador'),
)

BRAZIL_STATES = (
    # ('AC', 'Acre'),
    # ('AL', 'Alagoas'),
    # ('AP', 'Amapá'),
    # ('AM', 'Amazonas'),
    # ('BA', 'Bahia'),
    # ('CE', 'Ceará'),
    # ('DF', 'Distrito Federal'),
    # ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    # ('MA', 'Maranhão'),
    # ('MT', 'Mato Grosso'),
    # ('MS', 'Mato Grosso do Sul'),
    # ('MG', 'Minas Gerais'),
    # ('PA', 'Pará'),
    # ('PB', 'Paraíba'),
    # ('PR', 'Paraná'),
    # ('PE', 'Pernambuco'),
    # ('PI', 'Piauí'),
    # ('RJ', 'Rio de Janeiro'),
    # ('RN', 'Rio Grande do Norte'),
    # ('RS', 'Rio Grande do Sul'),
    # ('RO', 'Rondônia'),
    # ('RR', 'Roraima'),
    # ('SC', 'Santa Catarina'),
    # ('SP', 'São Paulo'),
    # ('SE', 'Sergipe'),
    # ('TO', 'Tocantins'),
)

COVERAGE_STUDIES_COMMUNICATION_TYPES = {
    '0': (
        ('0', 'Satélite'),
        ('1', 'Rede móvel 3G'),
        ('2', 'Rede móvel 3G com antena'),
        ('3', 'Rádio'),
        ('4', 'Fibra'),
    ),
    '1': (
        ('0', 'Satélite'),
        ('1', 'Rede Móvel 3G'),
        ('2', 'Rede Móvel 3G com antena'),
    ),
}

MOBILE_NETWORK_COMPANIES = (
    ('0', 'Claro'),
    ('1', 'Oi'),
    ('2', 'Tim'),
    ('3', 'Vivo'),
)

# electric points class
class ElectricPoints(models.Model):
    '''
    Electric Points
        class used to manage electric points
    '''

    # name used to identify electric points in workflow
    name = models.CharField(
        max_length=255, unique=True,
        blank=False, null=True, 
        verbose_name="Identificador único",
    )
    # type of equipment
    equipment_type = models.CharField(
        max_length=255,
        choices=EQUIPMENT_TYPE, 
        blank=False, null=True, 
        verbose_name="Tipo de equipamento",
    )
    # traceble feeder of this electric point
    feeder = models.ForeignKey(
        'electric_points.Feeders',
        on_delete=models.CASCADE,
        blank=False, null=True,
        verbose_name="Alimentador",
    )
    # traceble datetime of creation of electric point
    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=False, null=False, 
        verbose_name="Cadastrado em",
    )
    # traceble user that created electric point
    created_by = models.ForeignKey(
        'accounts.BasicUser',
        on_delete=models.CASCADE,
        blank=False, null=True, 
        verbose_name="Cadastrado por",
    )
    # location of the electric point
    locations = models.ManyToManyField(
        'electric_points.Locations',
        blank=True,
        verbose_name="Localização",
    )

    class Meta:
        db_table = 'electric_points'
        verbose_name = 'Ponto Elétrico'
        verbose_name_plural = 'Pontos Elétricos'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.name} ({self.get_equipment_type_display()})'

    def get_primary_key(self):
        return f'{self.id}'


# feeder class
class Feeders(models.Model):
    '''
    Feeders
        class used to manage Feeder objects
    '''

    # name used to identify feeder in workflow
    name = models.CharField(
        max_length=255,
        blank=False, null=True, 
        verbose_name="Identificador",
    )
    # amount of keys is being fed by the object
    key_amount = models.IntegerField(
        default=0, blank=True, null=True, 
        verbose_name="Quantidade de chaves",
    )
    # amount of reclosers is being fed by the object
    recloser_amount = models.IntegerField(
        default=0, blank=True, null=True, 
        verbose_name="Quantidade de religadores",
    )
    # name of the 'set' (group) this feeder is related
    set_name = models.CharField(
        max_length=255,
        blank=True, null=True, 
        verbose_name="Conjunto",
    )
    # the electric region this feeder belongs
    electric_region = models.CharField(
        max_length=255,
        blank=True, null=True, 
        verbose_name="Região elétrica",
    )

    class Meta:
        db_table = 'feeder'
        verbose_name = 'Alimentador'
        verbose_name_plural = 'Alimentadores'

    def __str__(self):
        return f'{self.name}'


# location class
class Locations(models.Model):
    '''
    Locations
        class used to manage the locations objects related to electric points
    '''
    # latitude of the location (e.g. -16.642649)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6,
        blank=False, null=True, 
        verbose_name="Latitude",
    )
    # longitude of the location (e.g. -49.542668)
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6,
        blank=False, null=True, 
        verbose_name="Longitude",
    )
    # city related to inputed coordenates
    city = models.CharField(
        max_length=255,
        choices=BRAZIL_GOIAS_CITIES, 
        blank=False, null=True, 
        verbose_name="Estado",
    )
    # stated related to inputed city
    state = models.CharField(
        max_length=255,
        choices=BRAZIL_STATES, 
        blank=False, null=True, 
        verbose_name="Estado",
    )
    # traceble date that location was created
    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=False, null=False, 
        verbose_name="Cadastrado em",
    )
    # traceble user that created the location
    created_by = models.ForeignKey(
        'accounts.BasicUser',
        on_delete=models.CASCADE,
        blank=False, null=True, 
        verbose_name="Cadastrado por",
    )
    # progress status that this is referenced
    progress_status = models.CharField(
        default='0',
        max_length=255,
        blank=False, null=False,
        choices=PROGRESS_STATUS,
        verbose_name="Etapa de referência",
    )
    # is this location obsolete in relation to the electric point
    obsolete = models.BooleanField(
        default=False, 
        blank=False, null=True,
        verbose_name="Posição obsoleta",
    )
    # city related to inputed coordenates
    related_electric_point_name = models.CharField(
        max_length=255,
        blank=True, null=True, 
        verbose_name="Ponto Elétrico obsoleto",
    )

    class Meta:
        db_table = 'locations'
        verbose_name = 'Localização'
        verbose_name_plural = 'Localizações'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id}'


# coverage studies class
class CoverageStudies(models.Model):
    '''
    Studies
        class used to manage the studies objects related to electric points
    '''

    # electric point related to the project
    electric_point = models.ForeignKey(
        'electric_points.ElectricPoints',
        on_delete=models.CASCADE,
        blank=False, null=True,
        verbose_name="Ponto Elétrico",
    )
    # study communication type
    communication_type = models.CharField(
        max_length=255,
        blank=True, null=True,
        verbose_name="Tipo de comunicação",
    )
    # traceble date that coverage study was created
    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=False, null=False, 
        verbose_name="Cadastrado em",
    )
    # traceble user that created the coverage study
    created_by = models.ForeignKey(
        'accounts.BasicUser',
        on_delete=models.CASCADE,
        blank=False, null=True, 
        verbose_name="Cadastrado por",
    )
    # mobile newtwork company name
    company_name = models.CharField(
        max_length=255,
        blank=True, null=True,
        choices=MOBILE_NETWORK_COMPANIES,
        verbose_name="Operadora",
    )
    # mobile network signal value
    mobile_signal = models.CharField(
        max_length=3,
        blank=True, null=True,
        verbose_name="Sinal",
    )

    class Meta:
        db_table = 'coverage_studies'
        verbose_name = 'Estudo Teórico de Cobertura'
        verbose_name_plural = 'Estudos Teóricos de Cobertura'

    def __str__(self):
        return f'{self.id}'


# class
class SupplyDelivery(models.Model):
    '''
    SupplyDelivery
        class used to manage the studies objects related to electric points
    '''

    # electric point related to the project
    electric_point = models.ForeignKey(
        'electric_points.ElectricPoints',
        on_delete=models.CASCADE,
        blank=False, null=True,
        verbose_name="Ponto Elétrico",
    )
    # study communication type
    communication_type = models.CharField(
        max_length=255,
        blank=True, null=True,
        verbose_name="Tipo de Comunicação",
    )
    # equipment communication type
    equipment_type = models.CharField(
        max_length=255,
        blank=True, null=True,
        verbose_name="Tipo de Equipamento",
    )
    # 
    code = models.CharField(
        max_length=255,
        blank=True, null=True,
        verbose_name="Código do Equipamento",
    )
    # 
    serial = models.CharField(
        max_length=255,
        blank=True, null=True,
        verbose_name="Número de Série",
    )
    # 
    internet_protocol_one = models.CharField(
        max_length=15,
        blank=True, null=True,
        validators=[MinLengthValidator(7)],
        verbose_name="IP Primário",
    )
    # 
    port_one = models.CharField(
        max_length=5,
        blank=True, null=True,
        validators=[MinLengthValidator(4)],
        verbose_name="Porta Primária",
    )
    # 
    internet_protocol_two = models.CharField(
        max_length=15,
        blank=True, null=True,
        validators=[MinLengthValidator(7)],
        verbose_name="IP Secundário",
    )
    # 
    port_two = models.CharField(
        max_length=5,
        blank=True, null=True,
        validators=[MinLengthValidator(4)],
        verbose_name="Porta Secundária",
    )
    # traceble date that coverage study was created
    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=False, null=False, 
        verbose_name="Cadastrado em",
    )
    # traceble user that created the coverage study
    created_by = models.ForeignKey(
        'accounts.BasicUser',
        on_delete=models.CASCADE,
        blank=False, null=True, 
        verbose_name="Cadastrado por",
    )

    class Meta:
        db_table = 'telecom_supply_delivery'
        verbose_name = 'Liberação de Materiais de Telecom'
        verbose_name_plural = 'Liberações de Materiais de Telecom'

    def __str__(self):
        return f'{self.id}'


# class
class FeederStudies(models.Model):
    '''
    FeederStudies
        class used to manage the studies objects related to electric points
    '''

    # electric point related to the project
    electric_point = models.ForeignKey(
        'electric_points.ElectricPoints',
        on_delete=models.CASCADE,
        blank=False, null=True,
        verbose_name="Ponto Elétrico",
    )
    # study communication type
    phase_adjustment = models.CharField(
        max_length=255,
        blank=True, null=True,
        verbose_name="Ajuste de Fase",
    )
    # 
    neutral_adjustment = models.CharField(
        max_length=255,
        blank=True, null=True,
        verbose_name="Ajuste de Neutro",
    )
    # 
    sensitive_neutral_adjustment = models.CharField(
        max_length=255,
        blank=True, null=True,
        verbose_name="Ajuste de Neutro Sensível",
    )
    # 
    shots = models.IntegerField(
        blank=True, null=True, 
        verbose_name="Número de Disparos",
    )
    # traceble date that coverage study was created
    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=False, null=False, 
        verbose_name="Cadastrado em",
    )
    # traceble user that created the coverage study
    created_by = models.ForeignKey(
        'accounts.BasicUser',
        on_delete=models.CASCADE,
        blank=False, null=True, 
        verbose_name="Cadastrado por",
        related_name="feeder_study_created_by"
    )
    # 
    applied = models.BooleanField(
        default=False,
        blank=False, null=True, 
        verbose_name="Implementado",
    )
    # traceble user that created the coverage study
    applied_by = models.ForeignKey(
        'accounts.BasicUser',
        on_delete=models.CASCADE,
        blank=True, null=True, 
        verbose_name="Implementado por",
        related_name="feeder_study_applied_by"
    )
    # traceble date that coverage study was created
    applied_at = models.DateTimeField(
        blank=True, null=True, 
        verbose_name="Implementado em",
    )

    class Meta:
        db_table = 'feeder_studies'
        verbose_name = 'Estudo de Alimentador'
        verbose_name_plural = 'Estudos de Alimentadores'

    def __str__(self):
        return f'{self.id}'
# -*- coding: utf-8 -*-
# python imports
import random
import re
# django imports
from django.conf import settings
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models

PROGRESS_STATUS = (
    ('0','A projetar'),
    ('1','A instalar'),
    ('2','A energizar'),
    ('3','A comissionar'),
    ('4','A operar'),
    ('5','Concluído'),
)

PENDENCIES_TYPES = {
    'installation': (
        ('0','Materiais de Obras'),
        # ('1','Materiais de Telecom'),
    ),
    'energizing': (
        ('0','Obra não concluída'),
    ),
    'commissioning': (
        ('0','Cobertura não condiz com estudo teórico'),
        ('1','Equipamento de Telecom com defeito'),
        ('2','Equipamento de MT com defeito'),
        ('3','Falta conectar MT'),
        ('4','IMS sem bateria'),
        ('5','Sem cadastro no mapa'),
        ('6','Tensão TP inadequada'),
    ),
    'operation': (
        ('0', 'Padrão'),
    ),
}

# projects class
class Projects(models.Model):
    '''
    Projects
        class used to create projects related to electric points
    '''

    # electric point related to the project
    electric_point = models.OneToOneField(
        'electric_points.ElectricPoints',
        on_delete=models.CASCADE,
        blank=True, null=True,
        verbose_name="Ponto Elétrico",
    )
    # project progress status
    progress_status = models.CharField(
        max_length=255, default="0",
        blank=False, null=False,
        choices=PROGRESS_STATUS,
        verbose_name="Etapa de referência",
    )
    # project execution request identifier
    sob = models.CharField(
        max_length=255, unique=True,
        blank=False, null=True,
        verbose_name="Número do Projeto",
    )
    # traceble datetime of project creation
    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=False, null=False,
        verbose_name="Cadastrado em",
    )
    # datetime that project was registred as finished
    finished_at = models.DateTimeField(
        blank=True, null=True,
        verbose_name="Data de conclusão",
    )
    # traceble user that created project
    created_by = models.ForeignKey(
        'accounts.BasicUser',
        on_delete=models.CASCADE,
        blank=False, null=True, 
        verbose_name="Cadastrado por",
        related_name="project_created_by"
    )
    # traceble user that created project
    finished_by = models.ForeignKey(
        'accounts.BasicUser',
        on_delete=models.CASCADE,
        blank=False, null=True, 
        verbose_name="Encerrado por",
        related_name="project_finished_by"
    )
    # linkable designing step
    designing = models.ForeignKey(
        'projects.Steps',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name="Projeto",
        related_name="project_project"
    )
    # linkable installation step
    installation = models.ForeignKey(
        'projects.Steps',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name="Instalação",
        related_name="project_installation"
    )
    # linkable energizing step 
    energizing = models.ForeignKey(
        'projects.Steps',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name="Energização",
        related_name="project_energizing"
    )
    # linkable comissioning step
    commissioning = models.ForeignKey(
        'projects.Steps',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name="Comissionamento",
        related_name="project_commissioning"
    )
    # linkable operation step
    operation = models.ForeignKey(
        'projects.Steps',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name="Operation",
        related_name="project_operation"
    )
    # all pendencies related to project
    pendencies = models.ManyToManyField(
        'projects.Pendencies',
        blank=True,
        verbose_name="Pendências",
        related_name="project_pendencies"
    )

    class Meta:
        db_table = 'projects'
        verbose_name = 'Projeto'
        verbose_name_plural = 'Projetos'

    def __str__(self):
        return f'{self.id}'

    def get_delay(self):
        if self.finished_at is not None:
            delta = self.finished_at - self.created_at
            if delta.days == 1:
                return f'{delta.days} dia'
            return f'{delta.days} dias'

        return None


# steps class
class Steps(models.Model):
    '''
    Steps
        class used to manage all project steps
    '''
    # related project to this step
    project = models.ForeignKey(
        'projects.Projects',
        on_delete=models.CASCADE,
        blank=True, null=True,
        verbose_name="Projeto",
        related_name="step_project"
    )
    # progress status that this is referenced
    progress_status = models.CharField(
        max_length=255,
        blank=False, null=False,
        choices=PROGRESS_STATUS,
        verbose_name="Etapa de referência",
    )
    # traceble user that created step
    created_by = models.ForeignKey(
        'accounts.BasicUser',
        on_delete=models.CASCADE,
        blank=False, null=True, 
        verbose_name="Cadastrado por",
    )
    # datetime that project step was registred
    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=True, null=False, 
        verbose_name="Cadastrado em",
    )
    # programmed finishing date of the project step
    programmed_date = models.DateTimeField(
        blank=False, null=True, 
        verbose_name="Data programada",
    )
    # real finishing date of the project step 
    real_date = models.DateTimeField(
        blank=False, null=True,
        verbose_name="Data de realização",
    )
    
    class Meta:
        db_table = 'steps'
        verbose_name = 'Etapa'
        verbose_name_plural = 'Etapas'

    def __str__(self):
        return f'{self.id}'

    def get_step_delay(self):
        if self.real_date is not None:
            delta = self.real_date - self.programmed_date
            if delta.days == 1:
                return f'{delta.days} dia'
            return f'{delta.days} dias'

        return None


# pendencies class
class Pendencies(models.Model):
    '''
    Pendencies
        class used to manage pendencies of project steps
    '''
    # related project to this step
    project = models.ForeignKey(
        'projects.Projects',
        on_delete=models.CASCADE,
        blank=True, null=True,
        verbose_name="Projeto",
        related_name="pendency_project"
    )
    # progress status that this is referenced
    pendency_type = models.CharField(
        max_length=255,
        blank=False, null=True,
        verbose_name="Tipo de pendência",
    )
    # progress status that this is referenced
    progress_status = models.CharField(
        max_length=255,
        blank=False, null=False,
        choices=PROGRESS_STATUS,
        verbose_name="Etapa de referência",
    )
    # optional description of project pendencies
    description = models.TextField(
        blank=False, null=True,
        verbose_name="Descrição",
    )
    # datetime that project pendency was registred
    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=True, null=False, 
        verbose_name="Cadastrada em",
    )
    # datetime that project pendency was registred
    solved_at = models.DateTimeField(
        blank=True, null=True, 
        verbose_name="Solucionada em",
    )
    # traceble user that created project pendency
    created_by = models.ForeignKey(
        'accounts.BasicUser',
        on_delete=models.CASCADE,
        blank=False, null=True, 
        verbose_name="Cadastrada por",
    )
    # boolean field to solve pendency
    solved = models.BooleanField(
        default=False,
        blank=False, null=False,
        verbose_name="Solucionada"
    )

    class Meta:
        db_table = 'pendencies'
        verbose_name = 'Pendência'
        verbose_name_plural = 'Pendências'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id}'

    def get_step_delay(self):
        if self.solved_at is not None:
            delta = self.solved_at - self.created_at
            if delta.days == 1:
                return f'{delta.days} dia'
            return f'{delta.days} dias'

        return None
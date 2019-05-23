# -*- coding: utf-8 -*-
# python imports
import random
import re
# django imports
from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models

PROFILES = (
    ('0','Administração'),
    ('1','Planejamento'),
    ('2','Projeto'),
    ('3','Obras'),
    ('4','Telecontrole'),
    ('5','Telecom'),
    ('6','Proteção'),
    ('7','Visualização'),
)

 
# super user class
class SuperUser(BaseUserManager):
    '''
    SuperUser:
        class used within './manage.py createsuperuser' command
        to create users on development level
    '''

    # function to set create superuser required fields
    def create_superuser(self, username, password):
        super_user = self.model(
            username=username,
            superuser=True,            
        )
        super_user.set_password(password)
        super_user.save(using=self.db)

        return super_user


def get_choices_index(choices, value):
    '''
    Function to get index of choices tuples by its value.
    '''
    choices_keys = list(dict(choices).keys())
    choices_values = list(dict(choices).values())

    return choices_keys[choices_values.index(value)]


# basic user class
class BasicUser(AbstractBaseUser, PermissionsMixin):
    '''
    BasicUser:
        class used to create all levels of end users of the project
    '''
    
    # field to set if user is active on project
    active = models.BooleanField(
        default=True,
        blank=False, null=False, 
        verbose_name="Ativo",
    )
    # traceble datetime of user creation
    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=False, null=False, 
        verbose_name="Cadastrado em",
    )
    # traceble user that created current user
    created_by = models.ForeignKey(
        'self',
        on_delete=models.CASCADE, 
        blank=False, null=True, 
        verbose_name="Cadastrado por",
    )
    # user email
    email = models.EmailField(
        max_length=255, unique=True, 
        blank=False, null=True, 
        verbose_name="Email",
    )
    # user first name
    first_name = models.CharField(
        max_length=255, 
        blank=False, null=True, 
        verbose_name="Primeiro nome",
    )
    # user last name
    last_name = models.CharField(
        max_length=255, 
        blank=False, null=True, 
        verbose_name="Último nome",
    )
    # username used to authenticate
    username = models.CharField(
        max_length=12, unique=True,
        blank=False, null=False,
        validators=[MinLengthValidator(12)],
        verbose_name="Usuário Enel",
    )
    # user permission profile
    profile = models.CharField(
        max_length=255, choices=PROFILES, 
        blank=False, null=False, 
        verbose_name="Perfil",
    )
    # user avatar image (last added is used as current active image)
    avatars = models.ManyToManyField(
        'accounts.Avatars', 
        blank=True, 
        verbose_name="Avatar",
    )
    # super user flag
    superuser = models.BooleanField(
        default=False, 
        blank=False, null=False, 
        verbose_name="Administrador",
    )
    objects = SuperUser()
    # set user filed to authenticate
    USERNAME_FIELD = 'username'
    # other required fileds
    # REQUIRED_FIELDS = ['']

    class Meta:
        db_table = 'Users'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __unicode__(self):
        return self.email

    @property
    def is_active(self):
        return self.active == 1

    @property
    def is_admin(self):
        return True if self.profile == get_choices_index(PROFILES, 'Administração') else False

    @property
    def is_planner(self):
        return True if self.profile == get_choices_index(PROFILES, 'Planejamento') else False

    @property
    def is_designer(self):
        return True if self.profile == get_choices_index(PROFILES, 'Projeto') else False
    
    @property
    def is_constructor(self):
        return True if self.profile == get_choices_index(PROFILES, 'Obras') else False

    @property
    def is_telecontrol(self):
        return True if self.profile == get_choices_index(PROFILES, 'Telecontrole') else False
    
    @property
    def is_telecom(self):
        return True if self.profile == get_choices_index(PROFILES, 'Telecom') else False

    @property
    def is_protection(self):
        return True if self.profile == get_choices_index(PROFILES, 'Proteção') else False

    @property
    def is_viewer(self):
        return True if self.profile == get_choices_index(PROFILES, 'Visualização') else False

    @property
    def is_staff(self):
        return self.superuser

    @property
    def is_superuser(self):
        return self.superuser

    @property
    def get_short_name(self):
        return self.username

    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'


def user_directory_path(instance, filename):
    '''
    Function to set upload filepath and filename.
    '''
    # check if file extension name matches regular expression
    extension = filename[-4:] if re.compile("(?:jpg|png)$").match(filename[-3:]) else 'nope'
    # File upload path: MEDIA_ROOT/BasicUser.id/<random name>
    return '{0}/{1:06d}.{2}'.format('media/img/avatars/', random.randint(0,999999), extension)


# avatar image class
class Avatars(models.Model):
    '''
    Avatar:
        avatar images for users
    '''
    
    # avatar image file
    avatar = models.ImageField(
        upload_to = user_directory_path,
        default = 'static/img/avatars/default.jpg', 
        blank=True, null=False,
        verbose_name="Avatar",
    )
    # traceble datetime of avatar upload
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        blank=False, null=False,
        verbose_name="Atualizado em",
    )

    class Meta:
        db_table = 'avatars'
        verbose_name = 'Avatar'
        verbose_name_plural = 'Avatares'

    def __str__(self):
        return f'{self.id}'
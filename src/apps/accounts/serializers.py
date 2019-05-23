# -*- coding: utf-8 -*-
#python imports
import re
# django imports
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, validators
# self imports
from .models import *


# 
class LoginSerializer(serializers.Serializer):
    '''
    '''
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        self.user = authenticate(
            None, 
            username=attrs.get('username', None), 
            password=attrs.get('password', None)
        )
        if not self.user:
            raise validators.ValidationError('Invalid')

        return attrs


# 
class UserSerializer(serializers.ModelSerializer):
    """
    User Serializer
    """
    class Meta:
        model = BasicUser
        fields = ('active','admin','username','email','superuser')

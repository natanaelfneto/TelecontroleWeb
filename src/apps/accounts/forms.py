# -*- coding: utf-8 -*-
# django imports
from django import forms
from django.contrib.auth import authenticate
# self imports
from .helpers import *
from .models import *


# form to render authenticate fileds
class LoginForm(forms.Form):
    '''
    Login Form
        form used in login page to authenticate users already created in database
    '''

    # username field
    username = forms.CharField(    
        widget=forms.TextInput(attrs={
            'autocomplete':'off',
            'placeholder':'Usuário Enel',
            'class':'form-control my-3',
            'maxlength':'12',
        })
    )

    # password field
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'autocomplete':'off',
            'placeholder':'Senha',
            'class':'form-control my-3'
        })
    )

    # get user object
    def get_user(self):
        return self.user

    # use helper file to fileds
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = LoginHelper()

        # turn off username and passowrd form labels visibility
        self.fields['username'].label = False
        self.fields['password'].label = False

    # clean function
    def clean(self):
        if self.errors:
            return super(LoginForm, self).clean()

        # get user from database
        user = BasicUser.objects.filter(username=self.cleaned_data['username'])

        # try match user authentication inputs with database users
        self.user = authenticate(
            username=self.cleaned_data.get('username', None),
            password=self.cleaned_data['password']
        )

        # standard message error for user and password mismatch
        error_message = u'Não foi possível autenticar este usuário'

        # if no user was found
        if user.count() == 0:    
            self.add_error('username', error_message)

        # if password hash for user do not macth
        if (not self.user or not self.user.active == 1) and self.cleaned_data.get('username', None):            
            self.add_error('username', error_message)

        return super(LoginForm, self).clean()


# form render fields for adding user
class UserForm(forms.ModelForm):
    '''
    User Forms
        form used when creating new users in database
    '''

    # avatar custom field to receive an image and create an avatar to be linked to user
    avatar_field = forms.ImageField(label='Avatar', required=False)

    # field to receive user desired passord
    password1 = forms.CharField(widget=forms.PasswordInput, label='Senha')

    # field to receive user desired password confirmation
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirmação de senha')

    class Meta:
        model = BasicUser
        fields = [
            # model fields
            'active',
            'email',
            'first_name',
            'last_name',
            'profile',
            'username',
            # custom fields
            'avatar_field',
            'password1',
            'password2',
        ]

    # use helper file to fileds
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = UserHelper()

        # 
        if self.instance.pk:
            # make custom fields for password and confirmation to not be required
            # when user already exist on database, i.e. user is being updated
            self.fields['password1'].required = False
            self.fields['password2'].required = False

    # get a cleared username filed
    def clean_username(self):
        # set all usernames created to be an uppercase string
        username = self.cleaned_data.get("username").upper()
        
        return username

    # get a cleared password fileds
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        # check if password and confirmation fields macth
        if password1 != password2:
            raise forms.ValidationError(u"As senhas não corresponderam")

    # save function
    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        if self.cleaned_data["password1"]:
            user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()

        return user


# for render to update users avatars
class AvatarsForm(forms.ModelForm):
    '''
    Avatar Form
        form used when users update their avatars images
    '''

    class Meta:
        model = Avatars 
        fields = ['avatar']

    def __init__(self, *args, **kwargs):
        super(AvatarsForm, self).__init__(*args, **kwargs)
        self.helper = AvatarsHelper()

    def save(self, commit=True):
        thisObject = super(AvatarsForm, self).save(commit=False)
        if commit:
            thisObject.save()
            self.save_m2m()
        return thisObject

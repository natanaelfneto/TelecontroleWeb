# -*- coding: utf-8 -*-
# django imports
from django import forms
from django.contrib.auth import authenticate
# self imports
from .helpers import *
from .models import *


# 
class ProjectsForm(forms.ModelForm):
    '''
    Projects Form
        form used to add new project object in database
        with custom field to add an installation step with programmed date
    '''

    # installation programmed date custom field
    programmed_date = forms.DateField(
        input_formats=settings.DATE_INPUT_FORMATS,
        label="Data programada de instalação",
    )

    class Meta:
        model = Projects 
        fields = [
            # model fields
            # 'electric_point',            
            'sob',
            # custom fields
            'programmed_date',
        ]

    def __init__(self, *args, **kwargs):
        super(ProjectsForm, self).__init__(*args, **kwargs)
        self.helper = ProjectsHelper()

    def save(self, commit=True):
        thisObject = super(ProjectsForm, self).save(commit=False)
        if commit:
            thisObject.save()
            self.save_m2m()
        return thisObject


class ProjectProgrammedDateForm(forms.ModelForm):
    '''
    Project Programmed Date Form
        form used to set programmed date for project step object in database
    '''

    # programmed date custom field
    programmed_date = forms.DateField(
        input_formats=settings.DATE_INPUT_FORMATS,
        label="Data programada",
    )

    class Meta:
        model = Projects 
        fields = [
            # custom fields
            'programmed_date',
        ]
 
    def __init__(self, *args, **kwargs):
        super(ProjectProgrammedDateForm, self).__init__(*args, **kwargs)
        self.helper = ProjectProgrammedDateHelper()

    def save(self, commit=True):
        thisObject = super(ProjectProgrammedDateForm, self).save(commit=False)
        if commit:
            thisObject.save()
            self.save_m2m()
        return thisObject


class ProjectRealDateForm(forms.ModelForm):
    '''
    Project Real Date Form
        form used to set real date for project step object in database
    '''

    # real date custom field
    real_date = forms.DateField(
        input_formats=settings.DATE_INPUT_FORMATS,
        label="Data real",
    )

    class Meta:
        model = Projects 
        fields = [
            # custom fields
            'real_date',
        ]
 
    def __init__(self, *args, **kwargs):
        super(ProjectRealDateForm, self).__init__(*args, **kwargs)
        self.helper = ProjectRealDateHelper()

    def save(self, commit=True):
        thisObject = super(ProjectRealDateForm, self).save(commit=False)
        if commit:
            thisObject.save()
            self.save_m2m()
        return thisObject


class DesigningPendenciesForm(forms.ModelForm):
    '''
    '''

    pendency_type = forms.ChoiceField(
        # choices=PENDENCIES_TYPES['designing']
    )
 
    class Meta:
        model = Pendencies 
        fields = ['pendency_type', 'description']
        
    def __init__(self, *args, **kwargs):
        super(DesigningPendenciesForm, self).__init__(*args, **kwargs)
        self.helper = PendenciesHelper()

    def save(self, commit=True):
        thisObject = super(DesigningPendenciesForm, self).save(commit=False)
        if commit:
            thisObject.save()
            self.save_m2m()
        return thisObject


class InstallationPendenciesForm(forms.ModelForm):
    '''
    '''

    pendency_type = forms.ChoiceField(
        choices=PENDENCIES_TYPES['installation']
    )
 
    class Meta:
        model = Pendencies 
        fields = ['pendency_type', 'description']
        
    def __init__(self, *args, **kwargs):
        super(InstallationPendenciesForm, self).__init__(*args, **kwargs)
        self.helper = PendenciesHelper()

    def save(self, commit=True):
        thisObject = super(InstallationPendenciesForm, self).save(commit=False)
        if commit:
            thisObject.save()
            self.save_m2m()
        return thisObject


class EnergizingPendenciesForm(forms.ModelForm):
    '''
    '''

    pendency_type = forms.ChoiceField(
        choices=PENDENCIES_TYPES['energizing']
    )
 
    class Meta:
        model = Pendencies 
        fields = ['pendency_type', 'description']
        
    def __init__(self, *args, **kwargs):
        super(EnergizingPendenciesForm, self).__init__(*args, **kwargs)
        self.helper = PendenciesHelper()

    def save(self, commit=True):
        thisObject = super(EnergizingPendenciesForm, self).save(commit=False)
        if commit:
            thisObject.save()
            self.save_m2m()
        return thisObject


class CommissioningPendenciesForm(forms.ModelForm):
    '''
    '''

    pendency_type = forms.ChoiceField(
        choices=PENDENCIES_TYPES['commissioning']
    )
 
    class Meta:
        model = Pendencies 
        fields = ['pendency_type', 'description']
        
    def __init__(self, *args, **kwargs):
        super(CommissioningPendenciesForm, self).__init__(*args, **kwargs)
        self.helper = PendenciesHelper()

    def save(self, commit=True):
        thisObject = super(CommissioningPendenciesForm, self).save(commit=False)
        if commit:
            thisObject.save()
            self.save_m2m()
        return thisObject


class OperationPendenciesForm(forms.ModelForm):
    '''
    '''

    pendency_type = forms.ChoiceField(
        choices=PENDENCIES_TYPES['operation']
    )
 
    class Meta:
        model = Pendencies 
        fields = ['pendency_type', 'description']
        
    def __init__(self, *args, **kwargs):
        super(OperationPendenciesForm, self).__init__(*args, **kwargs)
        self.helper = PendenciesHelper()

    def save(self, commit=True):
        thisObject = super(OperationPendenciesForm, self).save(commit=False)
        if commit:
            thisObject.save()
            self.save_m2m()
        return thisObject


class ProjectSobForm(forms.ModelForm):
    '''
    '''
 
    class Meta:
        model = Projects
        fields = ['sob',]
        
    def __init__(self, *args, **kwargs):
        super(ProjectSobForm, self).__init__(*args, **kwargs)
        self.helper = ProjectSobHelper()

    def save(self, commit=True):
        thisObject = super(ProjectSobForm, self).save(commit=False)
        if commit:
            thisObject.save()
            self.save_m2m()
        return thisObject


class ProjectOperativeNumberForm(forms.ModelForm):
    '''
    '''
 
    class Meta:
        model = Projects
        fields = ['operative_number',]
        
    def __init__(self, *args, **kwargs):
        super(ProjectOperativeNumberForm, self).__init__(*args, **kwargs)
        self.helper = ProjectOperativeNumberHelper()

    def save(self, commit=True):
        thisObject = super(ProjectOperativeNumberForm, self).save(commit=False)
        if commit:
            thisObject.save()
            self.save_m2m()
        return thisObject
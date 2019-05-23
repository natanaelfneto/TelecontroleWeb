# -*- coding: utf-8 -*-
# django imports
from django import forms
from django.contrib.auth import authenticate
from django.core.validators import MaxValueValidator, MinValueValidator
# self imports
from projects.models import Projects
from .helpers import *
from .models import *


# 
class ElectricPointsForm(forms.ModelForm):
    '''
    Electric Points Form
        form used to add new electric point objects in database
        with custom fields for auto adding related location
    '''

    # latitude of the location (e.g. -16.642649)
    latitude = forms.DecimalField(
        max_digits=9, decimal_places=6,
        label="Latitude",
        widget=forms.NumberInput(attrs={'placeholder': '-16.642649'})
    )
    # longitude of the location (e.g. -49.542668)
    longitude = forms.DecimalField(
        max_digits=9, decimal_places=6,
        label="Longitude",
        widget=forms.NumberInput(attrs={'placeholder': '-49.542668'})
    )
    # city related to inputed coordenates
    city = forms.ChoiceField(label="Cidade", choices=BRAZIL_GOIAS_CITIES, initial='95')
    # stated related to inputed city
    state = forms.ChoiceField(label="Estado", choices=BRAZIL_STATES, initial='GO')

    class Meta:
        model = ElectricPoints
        fields = [
            # model fields
            'name', 
            'equipment_type', 
            'feeder',
            # custom fields 
            'longitude', 
            'latitude', 
            'city', 
            'state'
        ]

    def __init__(self, *args, **kwargs):
        super(ElectricPointsForm, self).__init__(*args, **kwargs)
        self.helper = ElectricPointsHelper()

    def save(self, commit=True):
        thisObject = super(ElectricPointsForm, self).save(commit=False)
        if commit:
            thisObject.save()
            self.save_m2m()
        return thisObject


class FeedersForm(forms.ModelForm):
    '''
    Feeders Form
        forms to add new feeder objects to database
    '''

    class Meta:
        model = Feeders 
        fields = [
            'name', 
            'key_amount', 
            'recloser_amount',
            'set_name',
            'electric_region'
        ]

    def __init__(self, *args, **kwargs):
        super(FeedersForm, self).__init__(*args, **kwargs)
        self.helper = FeedersHelper()

    def save(self, commit=True):
        thisObject = super(FeedersForm, self).save(commit=False)
        if commit:
            thisObject.save()
            self.save_m2m()
        return thisObject


class LocationsForm(forms.ModelForm):
    '''
    Locations Forms
        form used to add new location objects to database
    '''
  
    related_electric_point_name = forms.ModelChoiceField(
        label="Ponto Elétrico",          
        queryset=ElectricPoints.objects.filter(projects__electric_point=None)
    )

    # latitude of the location (e.g. -16.642649)
    latitude = forms.DecimalField(
        max_digits=9, decimal_places=6,
        label="Latitude",
        widget=forms.NumberInput(attrs={'placeholder': '-16.642649'})
    )
    # longitude of the location (e.g. -49.542668)
    longitude = forms.DecimalField(
        max_digits=9, decimal_places=6,
        label="Longitude",
        widget=forms.NumberInput(attrs={'placeholder': '-49.542668'})
    )
    # city related to inputed coordenates
    city = forms.ChoiceField(label="Cidade", choices=BRAZIL_GOIAS_CITIES, initial='95')
    # stated related to inputed city
    state = forms.ChoiceField(label="Estado", choices=BRAZIL_STATES, initial='GO')

    class Meta:
        model = Locations 
        fields = [
            'related_electric_point_name',
            'longitude',
            'latitude',
            'city',
            'state'
        ]

    def __init__(self, *args, **kwargs):
        super(LocationsForm, self).__init__(*args, **kwargs)
        self.helper = LocationsHelper()

    def save(self, commit=True):
        thisObject = super(LocationsForm, self).save(commit=False)
        if commit:
            thisObject.save()
            self.save_m2m()
        return thisObject


class StartCoverageStudiesForm(forms.ModelForm):
    '''
    Coverage StudiesForms
        form used to add new coverage studies objects to database
    '''

    communication_type = forms.ChoiceField(
        label="Tipo de comunicação",
        choices=COVERAGE_STUDIES_COMMUNICATION_TYPES['0'],
    )

    class Meta:
        model = CoverageStudies 
        fields = [
            'communication_type',
        ]

    def __init__(self, *args, **kwargs):
        super(StartCoverageStudiesForm, self).__init__(*args, **kwargs)
        self.helper = StartCoverageStudiesHelper()

    def save(self, commit=True):
        thisObject = super(StartCoverageStudiesForm, self).save(commit=False)
        if commit:
            thisObject.save()
            self.save_m2m()
        return thisObject


class FinishesCoverageStudiesForm(forms.ModelForm):
    '''
    Coverage StudiesForms
        form used to add new coverage studies objects to database
    '''

    company_name = forms.ChoiceField(
        label="Operadora",
        choices=MOBILE_NETWORK_COMPANIES,
    )

    mobile_signal = forms.IntegerField(
        label="Sinal",
    )

    class Meta:
        model = CoverageStudies 
        fields = [
            'company_name',
            'mobile_signal'
        ]

    def __init__(self, *args, **kwargs):
        super(FinishesCoverageStudiesForm, self).__init__(*args, **kwargs)
        self.helper = FinishesCoverageStudiesHelper()

    def save(self, commit=True):
        thisObject = super(FinishesCoverageStudiesForm, self).save(commit=False)
        if commit:
            thisObject.save()
            self.save_m2m()
        return thisObject


class SupplyDeliveryForm(forms.ModelForm):
    '''
    SupplyDeliveryFormForms
        form used to add new coverage studies objects to database
    '''

    communication_type = forms.ChoiceField(
        label="Tipo de Comunicação",
        choices=COVERAGE_STUDIES_COMMUNICATION_TYPES['0'],
    )

    internet_protocol_one = forms.IntegerField(
        label="IP Primário",
        widget=forms.TextInput(attrs={
            'autocomplete':'off',
            'placeholder':'192.168.0.1',
            'maxlength':'15',
        })
    )

    port_one = forms.DecimalField(
        max_digits=5, decimal_places=0,
        label="Porta Primária",
        widget=forms.NumberInput(attrs={'placeholder': '80800'})
    )

    internet_protocol_two = forms.IntegerField(
        label="IP Secundário",
        widget=forms.TextInput(attrs={
            'autocomplete':'off',
            'placeholder':'192.168.0.1',
            'maxlength':'15',
        })
    )

    port_two = forms.DecimalField(
        max_digits=5, decimal_places=0,
        label="Porta Secundária",
        widget=forms.NumberInput(attrs={'placeholder': '80800'})
    )

    class Meta:
        model = SupplyDelivery 
        fields = [
            'communication_type',
            'equipment_type',
            'code',
            'serial',
            'internet_protocol_one',
            'port_one',
            'internet_protocol_two',
            'port_two'
        ]

    def __init__(self, *args, **kwargs):
        super(SupplyDeliveryForm, self).__init__(*args, **kwargs)
        self.helper = SupplyDeliveryHelper()

    def save(self, commit=True):
        thisObject = super(SupplyDeliveryForm, self).save(commit=False)
        if commit:
            thisObject.save()
            self.save_m2m()
        return thisObject


class FeederStudiesForm(forms.ModelForm):
    '''
    Feeder StudiesF orms
        form used to add new feeder studies objects to database
    '''

    class Meta:
        model = FeederStudies 
        fields = [
            'phase_adjustment',
            'neutral_adjustment',
            'sensitive_neutral_adjustment',
            'shots'
        ]

    def __init__(self, *args, **kwargs):
        super(FeederStudiesForm, self).__init__(*args, **kwargs)
        self.helper = FeederStudiesHelper()

    def save(self, commit=True):
        thisObject = super(FeederStudiesForm, self).save(commit=False)
        if commit:
            thisObject.save()
            self.save_m2m()
        return thisObject
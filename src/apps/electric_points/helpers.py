# -*- coding: utf-8 -*-
# crispy forms imports
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout, Submit, ButtonHolder


class ElectricPointsHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(ElectricPointsHelper, self).__init__(*args, **kwargs)

        self.layout = Layout(
            Div(
                Field('name', css_class="form-control"),
                css_class="form-group"
            ),
            Div(
                Field('equipment_type', css_class="form-control"),
                css_class="form-group"
            ),
            Div(
                Field('feeder', css_class="form-control"),
                css_class="form-group"
            ),
            Div(
                Field('longitude', css_class="form-control"),
                css_class="form-group"
            ),
            Div(
                Field('latitude', css_class="form-control"),
                css_class="form-group"
            ),
            Div(
                Field('city', css_class="form-control"),
                css_class="form-group"
            ),
            Div(
                Field('state', css_class="form-control"),
                css_class="form-group"
            ),
            Submit('submit', 'Submeter', css_class="float-right")
        )


class FeedersHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(FeedersHelper, self).__init__(*args, **kwargs)

        self.layout = Layout(
            Div(
                Field('name', css_class="form-control"),
                css_class="form-group"
            ),
            Div(
                Field('key_amount', css_class="form-control"),
                css_class="form-group"
            ),
            Div(
                Field('recloser_amount', css_class="form-control"),
                css_class="form-group"
            ),
            Div(
                Field('set_name', css_class="form-control"),
                css_class="form-group"
            ),
            Div(
                Field('electric_region', css_class="form-control"),
                css_class="form-group"
            ),
            Submit('submit', 'Submeter', css_class="float-right")
        )


class LocationsHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(LocationsHelper, self).__init__(*args, **kwargs)

        self.layout = Layout(
            Div(
                Field('related_electric_point_name', css_class="form-control"),
                css_class="form-group"
            ),
            Div(
                Field('latitude', css_class="form-control"),
                css_class="form-group d-none"
            ),
            Div(
                Field('longitude', css_class="form-control"),
                css_class="form-group d-none"
            ),
            Div(
                Field('city', css_class="form-control"),
                css_class="form-group d-none"
            ),
            Div(
                Field('state', css_class="form-control"),
                css_class="form-group d-none"
            ),
        )


class StartCoverageStudiesHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(StartCoverageStudiesHelper, self).__init__(*args, **kwargs)

        self.layout = Layout(
            Div(
                Field('communication_type', css_class="form-control"),        
                css_class="form-group",
            ),
        )


class FinishesCoverageStudiesHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(FinishesCoverageStudiesHelper, self).__init__(*args, **kwargs)

        self.layout = Layout(
            Div(
                Field('company_name', css_class="form-control"),        
                css_class="form-group",
            ),
            Div(
                Field('mobile_signal', css_class="form-control", min='0', max='100'),        
                css_class="form-group",
            ),
        )

    
class SupplyDeliveryHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(SupplyDeliveryHelper, self).__init__(*args, **kwargs)

        self.layout = Layout(
            Div(
                Field('communication_type', css_class="form-control"),        
                css_class="form-group",
            ),
            Div(
                Field('equipment_type', css_class="form-control",),        
                css_class="form-group",
            ),
            Div(
                Field('code', css_class="form-control",),        
                css_class="form-group",
            ),
            Div(
                Field('serial', css_class="form-control",),        
                css_class="form-group",
            ),
            Div(
                Div(
                    Field('internet_protocol_one', css_class="form-control", maxlength="15"),        
                    css_class="form-group col-8",
                ),
                Div(
                    Field('port_one', css_class="form-control", min='1000', max='99999'),
                    css_class="form-group col-4",
                ),
                css_class="row",
            ),
            Div(
                Div(
                    Field('internet_protocol_two', css_class="form-control", maxlength="15"),        
                    css_class="form-group col-8",
                ),
                Div(
                    Field('port_two', css_class="form-control", min='1000', max='99999'),        
                    css_class="form-group col-4",
                ),
                css_class="row",
            ),
        )


class FeederStudiesHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(FeederStudiesHelper, self).__init__(*args, **kwargs)

        self.layout = Layout(
            Div(
                Field('phase_adjustment', css_class="form-control"),        
                css_class="form-group",
            ),
            Div(
                Field('neutral_adjustment', css_class="form-control"),        
                css_class="form-group",
            ),
            Div(
                Field('sensitive_neutral_adjustment', css_class="form-control"),        
                css_class="form-group",
            ),
            Div(
                Field('shots', css_class="form-control"),        
                css_class="form-group",
            ),
        )

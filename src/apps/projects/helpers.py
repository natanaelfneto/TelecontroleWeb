# -*- coding: utf-8 -*-
# crispy forms imports
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout, Submit, ButtonHolder


class ProjectsHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(ProjectsHelper, self).__init__(*args, **kwargs)

        self.layout = Layout(
            Div(
                Field('electric_point', css_class="form-control"),
                css_class="form-group"
            ),
            Div(
                Field('programmed_date', css_class="form-control", autocomplete='off'),
                css_class="form-group"
            ),
            Div(
                Field('sob', css_class="form-control"),
                css_class="form-group"
            ),
            Submit('submit', 'Submeter', css_class="float-right")
        )


class ProjectProgrammedDateHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(ProjectProgrammedDateHelper, self).__init__(*args, **kwargs)

        self.layout = Layout(
            Div(
                Field('programmed_date', css_class="form-control", autocomplete='off'),
                css_class="form-group"
            ),
        )


class ProjectRealDateHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(ProjectRealDateHelper, self).__init__(*args, **kwargs)

        self.layout = Layout(
            Div(
                Field('real_date', css_class="form-control", autocomplete='off'),
                css_class="form-group"
            ),
        )


class PendenciesHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(PendenciesHelper, self).__init__(*args, **kwargs)

        self.layout = Layout(
            Div(
                Field('pendency_type', css_class="form-control", required=True,),
                css_class="form-group"
            ),
            Div(
                Field('description', css_class="form-control", required=True, rows="4"),
                css_class="form-group"
            ),
        )


# -*- coding: utf-8 -*-
# crispy forms imports
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout, Submit, ButtonHolder


class LoginHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(LoginHelper, self).__init__(*args, **kwargs)

        self.layout = Layout(
            Div(
                Field('username', maxlength="12"),
            ),
            Div(
                Field('password')
            )
        )


class UserHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(UserHelper, self).__init__(*args, **kwargs)

        self.layout = Layout(
            Div(
                Field('first_name', css_class="form-control"),
                css_class="form-group"
            ),
            Div(
                Field('last_name', css_class="form-control"),
                css_class="form-group"
            ),
            Div(
                Field('username', css_class="form-control"),
                css_class="form-group"
            ),
            Div(
                Field('email', css_class="form-control"),
                css_class="form-group"
            ),
            Div(
                Field('profile', css_class="form-control"),
                css_class="form-group"
            ),
            Div(
                Field('avatar_field', css_class="custom-file"),
                css_class="form-group"
            ),
            Field(
                'active', 
                css_class="custom-control-input", 
                template="crispy_fields/checkbox.html",
                value="true"
            ),
            Div(
                Field('password1', css_class="form-control"),
                css_class="form-group"
            ),
            Div(
                Field('password2', css_class="form-control"),
                css_class="form-group"
            ),
            Submit('submit', 'Submeter', css_class="float-right")
        )


class AvatarsHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(AvatarsHelper, self).__init__(*args, **kwargs)

        self.layout = Layout(
            Div(
                Field('avatar', css_class="form-control"),
                css_class="form-group"
            ),
            Submit('submit', 'Submeter', css_class="float-right")
        )


class UpdateUserPasswordHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(UpdateUserPasswordHelper, self).__init__(*args, **kwargs)

        self.layout = Layout(
            Div(
                Field('username', css_class="form-control"),
                css_class="form-group d-none"
            ),
            Div(
                Field('password0', css_class="form-control"),
                css_class="form-group"
            ),
            Div(
                Field('password1', css_class="form-control"),
                css_class="form-group"
            ),
            Div(
                Field('password2', css_class="form-control"),
                css_class="form-group"
            ),
            Submit('submit', 'Submeter', css_class="float-right")
        )

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django import forms
from .models import User, Profile

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class LoginForm(forms.ModelForm):
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'email',
            'password',
            Submit('submit', _('Sign in')),
        )

    class Meta:
        model = User
        fields=('email', 'password')


class UserForm(forms.ModelForm):
    email = forms.CharField(label='', max_length=100, widget=forms.EmailInput(attrs={'placeholder': _('Enter Email')}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': _('Enter Password')}))
    confirm_password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': _('Confirm Password')}))
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        # You can dynamically adjust your layout
        self.helper.layout.append(Submit('registration_submit', _('Sign Up')))
       
    class Meta:
        model = User
        fields=('email', 'password', 'confirm_password')

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                _("password and confirm password does not match")
            )

class ProfileForm(forms.ModelForm):
    t = """By checking the above button you agree with our <a href="/legality/"> Terms and Conditions </a>"""
    terms = forms.BooleanField(error_messages={'required': 
    'Please accept our terms and conditions to create account!'},
                               help_text=t)
    user_name = forms.CharField(error_messages={'exists': 
    'Username exists, please enter a different name.'},
                                max_length=20,)

    class Meta:
        model = Profile
        fields = ('user_name', 'contacto', 'data_nascimento', 'sexo', "terms")
        labels = {
            'terms': _("Our Terms and Conditions"),
        }

    def clean_user_name(self):
        cleaned_data = super(ProfileForm, self).clean()
        username = cleaned_data.get("user_name")
        duplicate_users = Profile.objects.filter(user_name=username)

        if duplicate_users.exists():
            raise ValidationError(_('Username exists, please enter a different name.'), code="exists")

        return username


class ProfileEditForm(forms.ModelForm):

    user_name = forms.CharField(error_messages={'exists': 'Username exists, please enter a different name.'},
                                max_length=20, )

    class Meta:
        model = Profile
        fields = ('user_name', 'contacto', 'data_nascimento', 'sexo')



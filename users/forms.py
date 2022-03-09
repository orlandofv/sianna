from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django import forms
from .models import User, Profile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model=User
        fields=('email', 'password', 'confirm_password')

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm password does not match"
            )


class ProfileForm(forms.ModelForm):
    t = """By checking the above button you agree with our <a href="/legality/"> Terms and Conditions </a>"""
    terms = forms.BooleanField(error_messages={'required': 'Please accept our terms and conditions to create account!'},
                               help_text=t)
    user_name = forms.CharField(error_messages={'exists': 'Username exists, please enter a different name.'},
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



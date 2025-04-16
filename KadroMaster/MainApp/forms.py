from django import forms
from django.forms import ModelForm
from MainApp.models import *
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Текущий пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите текущий пароль',
            'id': 'id_old_password'
        }),
        strip=False,
    )
    
    new_password1 = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите новый пароль',
            'id': 'id_new_password1'
        }),
        strip=False,
        help_text="Пароль должен содержать не менее 8 символов и не быть слишком простым.",
    )
    
    new_password2 = forms.CharField(
        label="Подтверждение нового пароля",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите новый пароль',
            'id': 'id_new_password2'
        }),
        strip=False,
    )

    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')
        try:
            validate_password(password1, self.user)
        except ValidationError as error:
            self.add_error('new_password1', error)
        return password1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'autofocus': True})
from django import forms
from django.forms import ModelForm
from MainApp.models import *

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
from .models import Accounts
from django import forms
from django.contrib.auth.forms import UserCreationForm


class AccountsForm(UserCreationForm):
    class Meta:
        model = Accounts
        fields = ('username', 'email', 'password1', 'password2', 'phone_number', 'type')


class LoginForm(forms.ModelForm):
    username = forms.CharField(label='اسم المستخدم')
    password = forms.CharField(
        label='كلمة المرور', widget=forms.PasswordInput())

    class Meta:
        model = Accounts
        fields = ('username', 'password')



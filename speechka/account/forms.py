from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from account.models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=100,
        label='Введите электронную почту',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите электронную почту'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваш пароль'})
    )


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

    first_name = forms.CharField(
        max_length=30,
        required=True,
        label='Имя',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваше имя'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label='Фамилия',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите вашу фамилию'})
    )
    username = forms.CharField(
        max_length=30,
        required=True,
        label='Имя пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя пользователя'})
    )
    email = forms.EmailField(
        required=True,
        label='Электронная почта',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваш email'})
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваш пароль'})
    )
    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите ваш пароль'})
    )
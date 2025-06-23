from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username',
            'password1', 'password2'
        ]
        labels = {
            'username': 'Имя пользователя',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'password': 'Пароль',
            'password2': 'Подтверждение пароля',
        }
        help_texts = {
            'username': 'Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.',
            'password2': 'Для подтверждения введите, пожалуйста, пароль ещё раз.',
        }


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        labels = {
            'username': 'Имя пользователя',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }

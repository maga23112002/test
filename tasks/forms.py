from django import forms
from .models import Task
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status']

class CustomLoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "Не правильный логин или пароль !"
    }


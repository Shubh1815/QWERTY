from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import Student

User = get_user_model()


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    username = forms.CharField(label=False, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Username',
        }
    ))
    password = forms.CharField(label=False, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        }
    ))


class StudentChangeForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('enrollment_no', 'std')

        widgets = {
            'enrollment_no': forms.TextInput(attrs={
                'readonly': True,
            }),
        }

        labels = {
            'std': 'Standard',
        }


class UserProfileChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'password1',
            'password2',
            'is_superuser',
            'is_manager'
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'password',
            'username',
            'first_name',
            'last_name',
            'is_superuser',
            'is_manager'
        )

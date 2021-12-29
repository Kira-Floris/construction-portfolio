from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from phonenumber_field.formfields import PhoneNumberField
from .models import *


class WebInfoForm(ModelForm):
	telephone = PhoneNumberField()

	class Meta:
		model = WebInfo
		fields = '__all__'


class UserRegisterForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class UserLoginForm(ModelForm):
	password = forms.CharField(label='password', widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = ['username', 'password']

class UserUpdateForm(ModelForm):
	class Meta:
		model = User
		fields = ['profile', 'email', 'username', 'first_name', 'last_name', 'bio']

class AdminUpdateForm(ModelForm):
	class Meta:
		model = User
		fields = ['profile', 'email', 'username', 'first_name', 'last_name', 'bio', 'role', 'position', 'display', 'is_active', 'is_staff', 'is_superuser', 'email_verified']

class UserAdminForm(ModelForm):
	class Meta:
		model = User
		fields = ['role', 'position', 'display', 'is_active', 'is_staff', 'is_superuser', 'email_verified']
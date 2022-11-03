from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import User


class UserRegisterForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('username','first_name','last_name','age','image','bio')


class UserChangeForma(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name','last_name','age','image','bio')
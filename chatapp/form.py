from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class UserForm(forms.ModelForm):
    password1=forms.CharField()
    password2=forms.CharField()
    class Meta:
        model=User
        fields = ['first_name','last_name' ,'email','password1','password2'] 


class ProfileUpdateForm(forms.ModelForm):
    email=forms.EmailField()
    class Meta:
        model=UserProfile
        fields=['email','first_name','last_name','profile_pic']
from .models import *
from django import forms
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User

class UserManagementForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

class UserAccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
        labels = {
            'first_name':('First Name'),
            'last_name':('Last Name'),
            'email':('Email'),
            'password':('Password'),
            
        }  
        widgets = {
            
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'password': forms.PasswordInput(),
            
            
        } 
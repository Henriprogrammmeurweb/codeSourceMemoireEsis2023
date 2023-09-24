from django import forms
from django.contrib.auth.forms import PasswordChangeForm


class FormLogin(forms.Form):
    email=forms.CharField(widget=forms.EmailInput(attrs={"class":'form-control'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":'form-control'}))


class FormChangePassword(PasswordChangeForm):
    old_password=forms.CharField(widget=forms.PasswordInput(attrs={"class":'form-control','placeholder':"Ancien mot de passe"}))
    new_password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":'form-control', 'placeholder':"Nouveau mot de passe"}))
    new_password2=forms.CharField(widget=forms.PasswordInput(attrs={"class":'form-control', 'placeholder':"Confirmer mot de passe"}))
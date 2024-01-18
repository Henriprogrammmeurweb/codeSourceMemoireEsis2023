from django import forms
from .import models
from django.contrib.auth.forms import (PasswordChangeForm,
                                       PasswordResetForm,
                                       SetPasswordForm)


class FormLogin(forms.Form):
    email=forms.CharField(widget=forms.EmailInput(attrs={"class":'form-control', 'placeholder':'Email'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":'form-control','placeholder':'Password'}))


class FormChangePassword(PasswordChangeForm):
    old_password=forms.CharField(widget=forms.PasswordInput(attrs={"class":'form-control'}))
    new_password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":'form-control'}))
    new_password2=forms.CharField(widget=forms.PasswordInput(attrs={"class":'form-control'}))

class Formpassword_reset(PasswordResetForm):
    email=forms.CharField(widget=forms.EmailInput(attrs={"class":'form-control', 'placeholder':'Email'}))


class FormSetPassword(SetPasswordForm):
    new_password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":'form-control', 'placeholder':'Nouveau Mot de passe'}))
    new_password2=forms.CharField(widget=forms.PasswordInput(attrs={"class":'form-control','placeholder':'Confirmer le Mot de passe'}))


class FormContact(forms.Form):
    nom=forms.CharField(widget=forms.TextInput(attrs={"class":'form-control'}))
    email=forms.CharField(widget=forms.EmailInput(attrs={"class":'form-control'}))
    message=forms.CharField(widget=forms.Textarea(attrs={"class":'form-control', 'rows':'3'}))


class ChangeProfilUser(forms.ModelForm):
    class Meta:
        model=models.Personnel

        fields=['photo']
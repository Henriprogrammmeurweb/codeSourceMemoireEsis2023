from django import forms
from .import models
from django.contrib.auth.forms import (PasswordChangeForm,
                                       PasswordResetForm,
                                       SetPasswordForm)


class FormLogin(forms.Form):
    """Formulaire de connexion du personnel"""
    email=forms.CharField(widget=forms.EmailInput(attrs={"class":'form-control', 'placeholder':'Email'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":'form-control','placeholder':'Password'}))
    se_souvenir_de_moi=forms.BooleanField(required=False)

class FormChangePassword(PasswordChangeForm):
    """Formulaire de changement de mot de passe du personnel"""
    old_password=forms.CharField(widget=forms.PasswordInput(attrs={"class":'form-control'}))
    new_password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":'form-control'}))
    new_password2=forms.CharField(widget=forms.PasswordInput(attrs={"class":'form-control'}))

class Formpassword_reset(PasswordResetForm):
    """Formulaire de demande de reinitialisation du mot de passe"""
    email=forms.CharField(widget=forms.EmailInput(attrs={"class":'form-control', 'placeholder':'Email'}))


class FormSetPassword(SetPasswordForm):
    """Formulaire de confirmation du nouveau mot de passe"""
    new_password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":'form-control', 'placeholder':'Nouveau Mot de passe'}))
    new_password2=forms.CharField(widget=forms.PasswordInput(attrs={"class":'form-control','placeholder':'Confirmer le Mot de passe'}))


class FormContact(forms.Form):
    """"Formulaire de Contact"""
    nom=forms.CharField(widget=forms.TextInput(attrs={"class":'form-control'}))
    email=forms.CharField(widget=forms.EmailInput(attrs={"class":'form-control'}))
    message=forms.CharField(widget=forms.Textarea(attrs={"class":'form-control', 'rows':'3'}))


class ChangeProfilUser(forms.ModelForm):
    """Formulaire de changement de photo de profil du personnel"""
    class Meta:
        model=models.Personnel

        fields=['photo']
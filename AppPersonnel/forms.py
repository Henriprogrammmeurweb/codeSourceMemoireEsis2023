from django import forms
from .import models
from AppAccount.models import Personnel




class FormAddService(forms.ModelForm):
    class Meta:
        model = models.Service
        fields = ["designation"]

        widgets = {"designation": forms.TextInput(attrs={"class": "form-control"})}


class EditerService(forms.ModelForm):
    class Meta:
        model = models.Service
        fields = ["designation"]

        widgets = {"designation": forms.TextInput(attrs={"class": "form-control"})}


class FormAddFonction(forms.ModelForm):
    class Meta:
        model = models.Fonction
        fields = ["service", "designation"]
        widgets = {
            "service": forms.Select(attrs={"class": "form-control"}),
            "designation": forms.TextInput(attrs={"class": "form-control"}),
        }


class FormEditerFonction(forms.ModelForm):
    class Meta:
        model = models.Fonction
        fields = ["service", "designation"]
        widgets = {
            "service": forms.Select(attrs={"class": "form-control"}),
            "designation": forms.TextInput(attrs={"class": "form-control"}),
        }


class FormAddGrade(forms.ModelForm):
    class Meta:
        model = models.Grade
        fields = ["designation"]
        widgets = {"designation": forms.TextInput(attrs={"class": "form-control"})}





class FormAddPersonnel(forms.ModelForm):
    class Meta:
        model = Personnel
        fields = [
            "matricule",
            "email",
            "username",
            "postnom",
            "prenom",
            "sexe",
            "grade",
            "fonction",
            "date_naissance",
            "date_engagement",
            "photo",
            "salaire",
            'prime',
            "etat_civil",
            "is_active",
            "is_superuser",
            "password",
            "demandeur",
            "approbateur",
            "consulteur",
            "sbgr",
            'planificateur'
        ]

        widgets = {
            "matricule": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "postnom": forms.TextInput(attrs={"class": "form-control"}),
            "prenom": forms.TextInput(attrs={"class": "form-control"}),
            "sexe": forms.Select(attrs={"class": "form-control"}),
            "grade": forms.Select(attrs={"class": "form-control"}),
            "fonction": forms.Select(attrs={"class": "form-control"}),
            "date_naissance": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "date_engagement": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "photo":forms.FileInput(attrs={"class": "form-control"}),
            "salaire": forms.Select(attrs={"class": "form-control"}),
            "prime": forms.Select(attrs={"class": "form-control"}),
            "etat_civil": forms.Select(attrs={"class": "form-control"}),
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
        }


class FormChangePersonnel(forms.ModelForm):
    class Meta:
        model = Personnel
        fields = [
            "matricule",
            "email",
            "username",
            "postnom",
            "prenom",
            "sexe",
            "grade",
            "fonction",
            "date_naissance",
            "date_engagement",
            "photo",
            "salaire",
            'prime',
            "etat_civil",
            "user_permissions",
            "is_active",
            "is_superuser",
            "demandeur",
            "approbateur",
            "consulteur",
            "sbgr",
            'planificateur'
        ]

        widgets = {
            "matricule": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "postnom": forms.TextInput(attrs={"class": "form-control"}),
            "prenom": forms.TextInput(attrs={"class": "form-control"}),
            "sexe": forms.Select(attrs={"class": "form-control"}),
            "grade": forms.Select(attrs={"class": "form-control"}),
            "fonction": forms.Select(attrs={"class": "form-control"}),
            "date_naissance": forms.TextInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "date_engagement": forms.TextInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "photo":forms.FileInput(attrs={"class": "form-control"}),
            "salaire": forms.Select(attrs={"class": "form-control"}),
            "prime": forms.Select(attrs={"class": "form-control"}),
            "etat_civil": forms.Select(attrs={"class": "form-control"}),
            "user_permissions": forms.SelectMultiple(attrs={"class": "form-control"}),
        }
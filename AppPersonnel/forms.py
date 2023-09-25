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


# class EditerGrade(forms.ModelForm):
#     class Meta:
#         model = models.Grade
#         fields = ["designation"]
#         widgets = {"designation": forms.TextInput(attrs={"class": "form-control"})}


# # class AddGroupePermission(forms.ModelForm):
# #     liste = Group.objects.all()

# #     class Meta:
# #         model = Group
# #         fields = ["name", "permissions"]
# #         widgets = {
# #             "name": forms.TextInput(attrs={"class": "form-control"}),
# #             "permissions": forms.SelectMultiple(attrs={"class": "form-control"}),
# #         }


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
            "sbgr"
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
            "sbgr"
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


# class FormPersonnelPermissions(forms.ModelForm):
#     class Meta:
#         model = models.Personnel
#         fields = [
#             "matricule",
#             "email",
#             "username",
#             "postnom",
#             "postnom",
#             "prenom",
#             "sexe",
#             "grade",
#             "fonction",
#             "date_naissance",
#             "date_engagement",
#             "photo",
#             "salaire",
#             "contact",
#             "etat_civil",
#             "role",
#             "is_staff",
#             "is_active",
#             "is_superuser",
#             "user_permissions",
#             "password",
#         ]

#         widgets = {
#             "matricule": forms.TextInput(attrs={"class": "form-control"}),
#             "email": forms.EmailInput(attrs={"class": "form-control"}),
#             "username": forms.TextInput(attrs={"class": "form-control"}),
#             "postnom": forms.TextInput(attrs={"class": "form-control"}),
#             "postnom": forms.TextInput(attrs={"class": "form-control"}),
#             "prenom": forms.TextInput(attrs={"class": "form-control"}),
#             "sexe": forms.Select(attrs={"class": "form-control"}),
#             "grade": forms.Select(attrs={"class": "form-control"}),
#             "fonction": forms.Select(attrs={"class": "form-control"}),
#             "date_naissance": forms.TextInput(attrs={"class": "form-control"}),
#             "date_engagement": forms.TextInput(attrs={"class": "form-control"}),
#             "salaire": forms.NumberInput(attrs={"class": "form-control"}),
#             "contact": forms.TextInput(attrs={"class": "form-control"}),
#             "etat_civil": forms.Select(attrs={"class": "form-control"}),
#             "role": forms.Select(attrs={"class": "form-control"}),
#             "user_permissions": forms.SelectMultiple(attrs={"class": "form-control"}),
#             "password": forms.TextInput(attrs={"class": "form-control"}),
#         }


# class AddApprobation(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(AddApprobation, self).__init__(*args, **kwargs)
#         conge_valide = models.Conge.objects.exclude(
#             id__in=models.Demande.objects.filter().values_list("conge__id", flat=True)
#         )
#         self.fields["conge"].queryset = conge_valide

#     class Meta:
#         model = models.Demande

#         fields = ["conge", "commentaire", "approbation", "date_debut", "date_fin"]
#         widgets = {
#             "conge": forms.Select(attrs={"class": "form-control"}),
#             "commentaire": forms.Textarea(attrs={"class": "form-control", "rows": "4"}),
#             "approbation": forms.CheckboxInput(attrs={"class": "form-control"}),
#             "date_debut": forms.DateInput(
#                 attrs={"class": "form-control", "type": "date"}
#             ),
#             "date_fin": forms.DateInput(
#                 attrs={"class": "form-control", "type": "date"}
#             ),
#         }


# class FormChangeApprobation(forms.ModelForm):
#     class Meta:
#         model = models.Demande

#         fields = ["conge", "commentaire", "approbation", "date_debut", "date_fin"]
#         widgets = {
#             "conge": forms.Select(attrs={"class": "form-control"}),
#             "commentaire": forms.Textarea(attrs={"class": "form-control", "rows": "4"}),
#             "approbation": forms.CheckboxInput(attrs={"class": "form-control"}),
#             "date_debut": forms.DateInput(attrs={"class": "form-control"}),
#             "date_fin": forms.DateInput(attrs={"class": "form-control"}),
#         }





# class ChangeFormConge(forms.ModelForm):
#     class Meta:
#         model = models.Conge
#         fields = ["titre", "motif"]
#         widgets = {
#             "titre": forms.TextInput(attrs={"class": "form-control"}),
#             "motif": forms.Textarea(attrs={"class": "form-control"}),
#         }


# class FormRetourConge(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         self.request = kwargs.pop("request")
#         super(FormRetourConge, self).__init__(*args, **kwargs)
#         conge_invalide = models.Demande.objects.exclude(approbation=False).exclude(
#             id__in=models.Retour.objects.filter().values_list("demande__id", flat=True)
#         )
#         self.fields["demande"].queryset = conge_invalide.filter(
#             conge__personnel=self.request.user
#         )

#     class Meta:
#         model = models.Retour
#         fields = ["demande", "confimer_retour"]
#         widgets = {
#             "demande": forms.Select(attrs={"class": "form-control"}),
#             "confimer_retour": forms.CheckboxInput(attrs={"class": "form-control"}),
#         }

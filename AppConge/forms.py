from django import forms
from .import models
import datetime


class FormAjoutConge(forms.ModelForm):
    class Meta:
        model = models.Conge
        fields = ["titre", "nature", "motif", "date_debut", "date_fin"]
        widgets = {
            "titre": forms.TextInput(attrs={"class": "form-control"}),
            "nature": forms.Select(attrs={"class": "form-control"}),
            "motif": forms.Textarea(attrs={"class": "form-control", "rows":"5"}),
            "date_debut": forms.TextInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "date_fin": forms.TextInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }





class FormAddApprobation(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormAddApprobation, self).__init__(*args, **kwargs)
        conge_valide = models.Conge.objects.exclude(id__in=models.Demande.objects.filter().values_list('conge__id', flat=True)).exclude(date_fin__lt=datetime.date.today())
        self.fields["conge"].queryset = conge_valide

    class Meta:
        model = models.Demande

        fields = ["conge", "commentaire", "approbation"]
        widgets = {
            "conge": forms.Select(attrs={"class": "form-control"}),
            "commentaire": forms.Textarea(attrs={"class": "form-control"}),
        }


class FormChangeApprobation(forms.ModelForm):
    class Meta:
        model = models.Demande

        fields = ["commentaire", "approbation"]
        widgets = {
            "commentaire": forms.Textarea(attrs={"class": "form-control", "rows": "5"}),
        }










    
    
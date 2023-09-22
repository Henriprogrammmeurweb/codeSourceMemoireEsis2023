from django import forms
from .import models


class FormAjoutConge(forms.ModelForm):
    class Meta:
        model = models.Conge
        fields = ["titre", "nature", "motif"]
        widgets = {
            "titre": forms.TextInput(attrs={"class": "form-control"}),
            "nature": forms.Select(attrs={"class": "form-control"}),
            "motif": forms.Textarea(attrs={"class": "form-control"}),
        }





class FormAddApprobation(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormAddApprobation, self).__init__(*args, **kwargs)
        conge_valide = models.Conge.objects.exclude(id__in=models.Demande.objects.filter().values_list('conge__id', flat=True))
        self.fields["conge"].queryset = conge_valide

    class Meta:
        model = models.Demande

        fields = ["conge", "commentaire", "approbation", "date_debut", "date_fin"]
        widgets = {
            "conge": forms.Select(attrs={"class": "form-control"}),
            "commentaire": forms.Textarea(attrs={"class": "form-control", "rows": "4"}),
            "approbation": forms.CheckboxInput(attrs={"class": "form-control"}),
            "date_debut": forms.TextInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "date_fin": forms.TextInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }


class FormChangeApprobation(forms.ModelForm):
    class Meta:
        model = models.Demande

        fields = ["commentaire", "approbation", "date_debut", "date_fin"]
        widgets = {
            "commentaire": forms.Textarea(attrs={"class": "form-control", "rows": "4"}),
            "approbation": forms.CheckboxInput(attrs={"class": "form-control"}),
            "date_debut": forms.TextInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "date_fin": forms.TextInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }


class FormRetourConge(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(FormRetourConge, self).__init__(*args, **kwargs)
        conge_invalide = models.Demande.objects.exclude(approbation=False).exclude(
            id__in=models.Retour.objects.filter().values_list("demande__id", flat=True)
        )
        self.fields["demande"].queryset = conge_invalide.filter(
            conge__personnel=self.request.user
        )

    class Meta:
        model = models.Retour
        fields = ["demande", "confimer_retour"]
        widgets = {
            "demande": forms.Select(attrs={"class": "form-control"}),
            "confimer_retour": forms.CheckboxInput(attrs={"class": "form-control"}),
        }






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


    
    
from django import forms
import datetime
from .import models


class FormAjoutPlanningConge(forms.ModelForm):
    global personnel
    def __init__(self, *args, **kwargs):
        self.request=kwargs.pop('request')
        super(FormAjoutPlanningConge, self).__init__(*args, **kwargs)
        service=models.Service.objects.filter(fonction__personnel=self.request.user)
        annee=models.Annee.objects.exclude(date_fin__lt=datetime.date.today())
        for i in service:
            personnel=models.Personnel.objects.filter(fonction__service=i)
        self.fields['personnel'].queryset=personnel
        self.fields['service'].queryset=service
        self.fields['annee'].queryset=annee
    class Meta:
        model=models.Planning

        fields=['personnel', 'nature','service','annee', 'date_debut','date_fin']

        widgets={
            "personnel":forms.Select(attrs={"class":"form-control"}),
            "nature":forms.Select(attrs={"class":"form-control"}),
            "service":forms.Select(attrs={"class":"form-control"}),
            "annee":forms.Select(attrs={"class":"form-control"}),
            "date_debut":forms.TextInput(attrs={"class":"form-control",'type':'date'}),
            "date_fin":forms.TextInput(attrs={"class":"form-control", 'type':'date'})
        }

class FormModifPlanningConge(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request=kwargs.pop('request')
        super(FormModifPlanningConge, self).__init__(*args, **kwargs)
        service=models.Service.objects.filter(fonction__personnel=self.request.user)
        annee=models.Annee.objects.exclude(date_fin__lt=datetime.date.today())
        for i in service:
            personnel=models.Personnel.objects.filter(fonction__service=i)
        self.fields['personnel'].queryset=personnel
        self.fields['service'].queryset=service
        self.fields['annee'].queryset=annee
    class Meta:
        model=models.Planning

        fields=['personnel', 'nature','service','annee', 'date_debut','date_fin']

        widgets={
            "personnel":forms.Select(attrs={"class":"form-control"}),
            "nature":forms.Select(attrs={"class":"form-control"}),
            "service":forms.Select(attrs={"class":"form-control"}),
            "annee":forms.Select(attrs={"class":"form-control"}),
            "date_debut":forms.TextInput(attrs={"class":"form-control",'type':'date'}),
            "date_fin":forms.TextInput(attrs={"class":"form-control", 'type':'date'})
        }



class FormAjoutAnnee(forms.ModelForm):
    class Meta:
        model=models.Annee

        fields=["designation","date_debut", "date_fin"]

        widgets={
            "designation":forms.TextInput(attrs={"class":"form-control"}),
            "date_debut":forms.TextInput(attrs={"class":"form-control",'type':'date'}),
            "date_fin":forms.TextInput(attrs={"class":"form-control", 'type':'date'})
        }
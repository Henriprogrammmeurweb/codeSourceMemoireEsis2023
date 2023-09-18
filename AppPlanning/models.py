from django.db import models
from AppAccount.models import Personnel
from AppConge.models import Conge
from AppPersonnel.models import Service


class Annee(models.Model):
    designation=models.CharField(max_length=155, unique=True)
    date_debut=models.DateField()
    date_fin=models.DateField()
    date_creation=models.DateTimeField(auto_now_add=True)
    date_modification=models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.designation


class Planning(models.Model):
    NATURE_CONGE = (
        ("Annuel", "Annuel"),
    )
    personnel=models.ForeignKey(Personnel, on_delete=models.SET_NULL, blank=True, null=True)
    nature = models.CharField(max_length=155, choices=NATURE_CONGE)
    service=models.ForeignKey(Service, on_delete=models.CASCADE)
    annee=models.ForeignKey(Annee, on_delete=models.CASCADE)
    date_debut=models.DateField()
    date_fin=models.DateField()
    date_creation=models.DateTimeField(auto_now_add=True)
    date_modification=models.DateTimeField(auto_now=True)



    @property
    def getNombreJours(self):
        return self.date_fin - self.date_debut
    
    def __str__(self):
        return self.nature


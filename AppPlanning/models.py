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


    @property
    def get_anneePlannig(self):
        planning=self.planning_set.all()
        liste_annee=[ligne.annee for ligne in planning]
        return liste_annee


    def __str__(self):
        return self.designation


class Planning(models.Model):
    personnel=models.ForeignKey(Personnel, on_delete=models.SET_NULL, blank=True, null=True)
    service=models.ForeignKey(Service, on_delete=models.SET_NULL, blank=True, null=True)
    annee=models.ForeignKey(Annee, on_delete=models.CASCADE)
    date_debut=models.DateField()
    date_fin=models.DateField()
    date_creation=models.DateTimeField(auto_now_add=True)
    date_modification=models.DateTimeField(auto_now=True)



    @property
    def getNombreJours(self):
        return self.date_fin - self.date_debut
    
    def save(self, *args, **kwargs):
        if not self.service :
            self.service = self.personnel.fonction.service
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.annee.designation


import datetime
from django.db import models
from AppAccount.models import Personnel
from AppConge.models import Conge
from AppPersonnel.models import Service


class Annee(models.Model):
    """Cette classe permet de stocker les années afin de planifier les congés"""
    designation=models.CharField(max_length=155, unique=True)
    date_debut=models.DateField()
    date_fin=models.DateField()
    date_creation=models.DateTimeField(auto_now_add=True)
    date_modification=models.DateTimeField(auto_now=True)


    @property
    def get_anneePlannig(self):
        """cette Méthode permet de recuperer la liste des annnées"""
        planning=self.planning_set.all()
        liste_annee=[ligne.annee for ligne in planning]
        return liste_annee


    def __str__(self):
        return self.designation


class Planning(models.Model):
    """"Cette classe sert à stocker les planifications des congés"""
    personnel=models.ForeignKey(Personnel, on_delete=models.PROTECT)
    service=models.ForeignKey(Service, on_delete=models.PROTECT, blank=True, null=True)
    annee=models.ForeignKey(Annee, on_delete=models.CASCADE)
    date_debut=models.DateField()
    date_fin=models.DateField()
    date_creation=models.DateTimeField(auto_now_add=True)
    date_modification=models.DateTimeField(auto_now=True)

    class Meta:
        ordering=['-date_creation']



    @property
    def getNombreJours(self):
        """Cette méthode permet de calculer le nombre de jour pour chaque planning"""
        nombre_jour = f'{self.date_fin - self.date_debut}'.split()
        return f'{nombre_jour[0]} jours'
        
    
    @property
    def getCongePlanningFini(self):
        """Cette Méthode permet de verifier si la date de fin d'une planification est depassée alors modif et delete impossible !"""
        if self.date_fin < datetime.date.today():
            return "Interdit"

    
    def save(self, *args, **kwargs):
        """Cette Méthode s'appelle à chaque planning pour le service du personnel"""
        if not self.service :
            self.service = self.personnel.fonction.service
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.annee.designation} {self.service.designation} {self.personnel.sexe}"


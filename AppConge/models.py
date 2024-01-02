from django.template.defaultfilters import slugify
from django.db import models
from AppAccount.models import Personnel
from datetime import date
import datetime


class Conge(models.Model):
    personnel = models.ForeignKey(Personnel, on_delete=models.PROTECT)
    titre = models.CharField(max_length=255)
    NATURE_CONGE = (
        ("Circonstance", "Circonstance"),
        ("Maternité", "Maternité"),
        ("Cumulé", "Cumulé"),
        ("A valoir", "A valoir"),
    )
    nature = models.CharField(max_length=155, choices=NATURE_CONGE)
    motif = models.TextField()
    date_debut = models.DateField()
    date_fin = models.DateField()
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_creation"]

    def __str__(self):
        return f"Agent: {self.personnel} Titre {self.titre}"

    @property
    def get_conge_demander(self):
        liste_conge_demande = self.demande_set.all()
        return [ligne.conge for ligne in liste_conge_demande]

    @property
    def getReponseConge(self):
        conge_demande = self.demande_set.all()
        reponse = [ligne.approbation for ligne in conge_demande]
        for i in reponse:
            if i == True:
                return "Congé accordé ✅"
            return "Congé rejeté ❌"

    @property
    def getNombreJours(self):
        total = self.date_fin - self.date_debut
        return total

    @property
    def getCommentaire(self):
        demande = self.demande_set.all()
        liste_formate = ""
        commentaire = [ligne.commentaire for ligne in demande]
        if commentaire:
            liste_formate = " ,".join(commentaire)
            return liste_formate
        return "-"



    @property
    def get_JoursConsomes(self):
        demande = self.demande_set.all()
        reponse = [ligne.approbation for ligne in demande]
        for reponses in reponse:
            if reponses == False:
                return 0
            elif reponses == True and self.date_debut == self.date_fin:
                return 1
            elif self.date_debut > date.today() and reponses == True:
                return "dans le futur"
            elif reponses == True and self.date_fin > date.today():
                return date.today() - self.date_debut
            elif reponses == True and self.date_fin == date.today():
                return self.date_fin - self.date_debut
            elif reponses == True and self.date_fin < date.today():
                return self.date_fin - self.date_debut
            else:
                return 0
        return "Demande encours"


class Demande(models.Model):
    conge = models.ForeignKey(Conge, on_delete=models.CASCADE)
    commentaire = models.TextField()
    approbation = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_creation"]

    def __str__(self):
        return f"Congé : {self.conge.titre}"



    @property
    def getReponseConge(self):
        if self.approbation == True:
            return "Congé accordé ✅"
        return "Congé rejeté ❌"




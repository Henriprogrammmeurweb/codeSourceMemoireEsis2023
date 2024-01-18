from django.template.defaultfilters import slugify
from django.db import models
from AppAccount.models import Personnel
from datetime import date
import datetime


class Conge(models.Model):
    """Classe de stocker les demandes des Congés des Personnels"""
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
        """Cette Méthode vérifie si au moins le congé a déjà une réponse"""
        liste_conge_demande = self.demande_set.all()
        return [ligne.conge for ligne in liste_conge_demande]

    @property
    def getReponseConge(self):
        """Cette Méthodes verfie aussi comme la 1ère et vérifie aussi si le délai est dépassé"""
        conge_demande = self.demande_set.all()
        reponse = [ligne.approbation for ligne in conge_demande]
        for reponses in reponse:
            if reponses == True:
                return "Congé accordé ✅"
            return "Congé rejeté ❌"
        if not self.id in reponse and self.date_fin < datetime.date.today():
            return "Aucune réponse 🔕"

    @property
    def getNombreJours(self):
        """Cette Méthodes calcul les nombres des jours pour chaque instance"""
        total = self.date_fin - self.date_debut
        return total

    @property
    def getCommentaire(self):
        """Cette Méthode recupère les commentaires aux demandes des congés"""
        demande = self.demande_set.all()
        liste_formate = ""
        commentaire = [ligne.commentaire for ligne in demande]
        if commentaire:
            liste_formate = " ,".join(commentaire)
            return liste_formate
        return "-"



    @property
    def get_JoursConsomes(self):
        """Cette Méthode permet de compter le nombres de jour consommés"""
        demande = self.demande_set.all()
        reponse = [ligne.approbation for ligne in demande]
        for reponses in reponse:
            if reponses == False:
                return f"0 Jour"
            elif reponses == True and self.date_debut == self.date_fin:
                return f"1 Jour"
            elif self.date_debut > date.today() and reponses == True:
                return f"Pas encore"
            elif reponses == True and self.date_fin > date.today():
                return date.today() - self.date_debut
            elif reponses == True and self.date_fin == date.today():
                return self.date_fin - self.date_debut
            elif reponses == True and self.date_fin < date.today():
                return self.date_fin - self.date_debut
            else:
                return 0
        if not self.id in reponse and self.date_fin < datetime.date.today():
            return "Delai depassé"
        return "Demande encours"


class Demande(models.Model):
    """Cette de stocker les réponses aux demandes des congés des Personnels"""
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
        """Cette Méthode permet de récuperer les réponses de congé"""
        if self.approbation == True:
            return "Congé accordé ✅"
        return "Congé rejeté ❌"




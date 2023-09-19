from django.template.defaultfilters import slugify
from django.db import models
from AppAccount.models import Personnel
from datetime import date
import datetime



class Conge(models.Model):
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE)
    titre = models.CharField(max_length=255)
    NATURE_CONGE = (
        ("Circonstance", "Circonstance"),
        ("Maternité", "Maternité"),
        ("Cumulé", "Cumulé"),
        ("A valoir", "A valoir"),
    )
    nature = models.CharField(max_length=155, choices=NATURE_CONGE)
    motif = models.TextField()
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
        conge_demande=self.demande_set.all()
        reponse=[ligne.approbation for ligne in conge_demande]
        for i in reponse:
            if i == True:
                return 'Congé accordé ✅'
            return 'Congé rejeté ❌'

    @property
    def getNombreJours(self):
        demande = self.demande_set.all()
        liste_formate=""
        nombre=[str(ligne.get_nombre_Jours) for ligne in demande]
        if len(nombre) == 0:
            return 0
        elif len(nombre) > 0 :
            liste_formate = ", ".join(nombre)
            return liste_formate
        else:
            return "-"
    
    @property
    def getCommentaire(self):
        demande = self.demande_set.all()
        liste_formate=""
        commentaire=[ligne.commentaire for ligne in demande]
        if commentaire:
            liste_formate = ' ,'.join(commentaire)
            return liste_formate
        return '-'

    @property
    def get_reste_jours(self):
        demande=self.demande_set.all()
        liste_formate=""
        reste_jours=[str(ligne.get_reste_jours) for ligne in demande]
        if reste_jours:
            liste_formate = ", ".join(reste_jours)
            return liste_formate
        return "-"

    @property
    def get_JoursConsomes(self):
       demande=self.demande_set.all()
       liste_formate=""
       jours=[str(ligne.getJoursConsommes) for ligne in demande]
       if jours:
            liste_formate = ",".join(jours)
            return liste_formate 
       return '-' 

        


class Demande(models.Model):
    conge = models.ForeignKey(Conge, on_delete=models.CASCADE)
    commentaire = models.TextField()
    approbation = models.BooleanField(default=False)
    date_debut = models.DateField()
    date_fin = models.DateField()
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_creation"]

    def __str__(self):
        return f"Congé : {self.conge.titre}"

    @property
    def get_nombre_Jours(self):
        if self.date_fin == self.date_debut :
            return 0
        return self.date_fin - self.date_debut
        

    @property
    def get_reste_jours(self):
        total_number = self.date_fin - date.today()
        if self.date_debut == self.date_fin:
            return self.date_fin - self.date_debut
        elif date.today() > self.date_fin:
            return self.date_fin - self.date_debut
        else:
            return total_number
    
    @property
    def getJoursConsommes(self):
        total=self.date_fin - self.date_debut
        if self.date_debut == self.date_fin:
            return 0
        elif date.today() == self.date_fin or date.today() > self.date_fin:
            return total
        else:
            return date.today() - self.date_debut
        
 




class Retour(models.Model):
    demande = models.ForeignKey(Demande, on_delete=models.CASCADE)
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE)
    confimer_retour = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_creation"]

    def __str__(self):
        return self.demande.conge.titre

    @property
    def get_nombreJours(self):
        date_jours = self.demande.date_fin - self.demande.date_debut
        return date_jours
    


    @property
    def get_retard(self):
        get_my_date_retard = (
            self.date_creation.date() - self.demande.date_creation.date()
        )
        return get_my_date_retard
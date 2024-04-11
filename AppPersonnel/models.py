import datetime
from django.db import models


class Grade(models.Model):
    """Cette classe permet de stocker les grades des Personnels"""
    designation = models.CharField(max_length=255, unique=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.designation

    @property
    def getNumberPersonMale(self):
        list_user=self.personnel_set.all()
        number_person=len([ligne.sexe for ligne in list_user if ligne.sexe == "M"])
        return number_person
    
    @property
    def getNumberPersonFemale(self):
        list_user=self.personnel_set.all()
        number_person=len([ligne.sexe for ligne in list_user if ligne.sexe == "F"])
        return number_person
    
    @property
    def TotalNumberPerson(self):
        number_total_person=self.getNumberPersonMale + self.getNumberPersonFemale
        return number_total_person

class Service(models.Model):
    """Cette classe permet de stocker les services de l'entreprise"""
    designation = models.CharField(max_length=255)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.designation


    @property
    def getNumberPersonMale(self):
        list_user=self.fonction_set.all()
        number_person=sum([ligne.getNumberPersonMale for ligne in list_user])
        return number_person
    
    @property
    def getNumberPersonFemale(self):
        list_user=self.fonction_set.all()
        number_person=sum([ligne.getNumberPersonFemale for ligne in list_user])
        return number_person
    
    @property
    def TotalNumberPerson(self):
        number_total_person=self.getNumberPersonMale + self.getNumberPersonFemale
        return number_total_person


class Fonction(models.Model):
    """Cette classe permet de stocker les fonctions des Personnels"""
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    designation = models.CharField(max_length=255)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.designation


    @property
    def getNumberPersonMale(self):
        list_user=self.personnel_set.all()
        number_person=len([ligne.sexe for ligne in list_user if ligne.sexe == "M"])
        return number_person
    
    @property
    def getNumberPersonFemale(self):
        list_user=self.personnel_set.all()
        number_person=len([ligne.sexe for ligne in list_user if ligne.sexe == "F"])
        return number_person
    
    @property
    def TotalNumberPerson(self):
        number_total_person=self.getNumberPersonMale + self.getNumberPersonFemale
        return number_total_person


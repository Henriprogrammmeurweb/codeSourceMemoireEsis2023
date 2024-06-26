from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
from AppPersonnel.models import Grade, Fonction




class Personnel(AbstractUser):
    """Classe permet de stocker les informations des personnels"""
    username=models.CharField(max_length=155)
    postnom=models.CharField(max_length=155)
    prenom=models.CharField(max_length=155)
    email=models.EmailField(max_length=155, unique=True)
    TYPE_SEXE = (("M", "M"), ("F", "F"))
    ETAT_CIVIL = (("M", "M"), ("C", "C"), ("V", "V"))
    SALAIRE=(
        ('Oui', 'Oui'),('Non', 'Non')
    )
    PRIME=(
        ('Oui', 'Oui'),('Non',"Non")
    )
    matricule = models.CharField(max_length=255, unique=True, blank=True, null=True)
    sexe = models.CharField(max_length=1, choices=TYPE_SEXE, default="M")
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT,blank=True, null=True)
    fonction = models.ForeignKey(Fonction, on_delete=models.PROTECT,blank=True, null=True)
    date_naissance = models.DateField(blank=True, null=True)
    date_engagement = models.DateField(blank=True, null=True)
    photo = models.ImageField(blank=True, null=True)
    salaire = models.CharField(max_length=3, choices=SALAIRE, default="Non")
    prime = models.CharField(max_length=3, choices=PRIME, default="Non")
    etat_civil = models.CharField(max_length=1, choices=ETAT_CIVIL, default='C')
    demandeur=models.BooleanField(default=False)
    approbateur=models.BooleanField(default=False)
    consulteur=models.BooleanField(default=False)
    sbgr=models.BooleanField(default=False)
    planificateur=models.BooleanField(default=False)
    date_creation=models.DateTimeField(auto_now_add=True)
    date_modification=models.DateTimeField(auto_now=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username', 'postnom', 'prenom',"sexe","etat_civil"]


    def __str__(self):
        return f"{self.username} {self.postnom} {self.prenom}"
    
    @property
    def getPersonnel(self):
        """Cette méthode permet de recuperer les personnels"""
        return f'{self.username} {self.postnom} {self.prenom}'

    @property
    def getPersonnelLogin(self):
        """Cette méthode permet de recuperer les personnels"""
        return f'{self.prenom.lower()} {self.username.lower()}'

    @property
    def getNombreDemandeConge(self):
        conge_user=self.conge_set.all()
        number_total=len([ligne.personnel for ligne in conge_user])
        return number_total

       
    

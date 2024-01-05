from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from AppAccount.models import Personnel
from ProjectGestionPersonnel.settings import EMAIL_HOST_USER
from .import models


# @receiver(post_save, sender=models.Planning)
# def sendEmailCreatePlanning(sender, created,instance, **kwargs):
#     if created:  
#         sujet=f"Planification des Congés"
#         message=f"Salut {instance.personnel.getPersonnel}, vous recevez ce message venant de la Division Provinciale du Haut-Katanga parce que votre congé de l'année : {instance.annee} a été planifié.\n La date de début : {instance.date_debut};\n La date de fin : {instance.date_fin}.\n N'hesitez pas de vous connecter sur la Plateforme pour plus d'Information"
#         send_mail(sujet, message,"", [instance.personnel.email])



# @receiver(post_save, sender=models.Planning)
# def sendEmailChangePlanning(sender, created,instance, **kwargs):
#     if not created:  
#         sujet=f"Changement de Planification des Congés"
#         message=f"Salut {instance.personnel.getPersonnel}, vous recevez ce message venant de la Division Provinciale du Haut-Katanga parce que votre congé de l'année : {instance.annee} a été modifié après la décision prise précédemment.\n La date de début : {instance.date_debut};\n La date de fin : {instance.date_fin}.\n N'hesitez pas de vous connecter sur la Plateforme pour plus d'Information"
#         send_mail(sujet, message,"", [instance.personnel.email])
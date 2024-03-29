from django.db.models.signals import post_save, pre_save
from django.core.mail import send_mail
from django.dispatch import receiver
from .import models
from AppAccount.models import Personnel
from ProjectGestionPersonnel.settings import EMAIL_HOST_USER


# @receiver(post_save, sender=models.Conge)
# def sendEmailCreateConge(sender, created,instance, **kwargs):
#     """Signal d'ajout d'email aux approbateurs lors de la demande des Congés"""
#     liste_Approbateur=[]
#     if created:
#         approbateur=Personnel.objects.filter(approbateur=True)
#         for i in approbateur:
#             liste_Approbateur.append(i.email)
#             sujet=f"Demande de congé du Personnel {instance.personnel.getPersonnel}"
#             message=f"Salut cher Approbateur, vous recevez ce message parce que l'Agent {instance.personnel.getPersonnel} vient de demander un congé de nature : {instance.nature}.\nVeuillez lui fournir une réponse rapidement, Cordialement"
#             send_mail(sujet, message,"", liste_Approbateur)




# @receiver(post_save, sender=models.Conge)
# def sendEmailChangeConge(sender, created,instance, **kwargs):
#     """Signals d'ajout d'émail aux appprobateurs quand on modifie la demande des congés"""
#     liste_Approbateur=[]
#     if not created:
#         approbateur=Personnel.objects.filter(approbateur=True)
#         for i in approbateur:
#             liste_Approbateur.append(i.email)
#             sujet=f"Demande de congé du Personnel {instance.personnel.username}-{instance.personnel.prenom}"
#             message=f"Salut cher Approbateur, vous recevez ce message parce que un Agent {instance.personnel.getPersonnel} vient de changer le congé qu'il avait demandé précedement : {instance.nature}.\nVeuillez lui fournir une réponse rapidement, Cordialement"
#             send_mail(sujet, message,"", liste_Approbateur)



# @receiver(post_save, sender=models.Demande)
# def sendEmailAddReponseDemande(sender, created,instance, **kwargs):
#     """Signal d'envoi d'email au demandeur des congé quand sa demande a été traitée"""
#     if created:
#         sujet=f"Réponse à votre demande de congé"
#         message=f"Salut, Vous recevez ce message parce que votre demande de congé a été traitée : {instance.conge.nature}.\Veuillez vous connecter sur le site pour plus de des détails.\nMerci Cordialement"
#         send_mail(sujet, message,"", [instance.conge.personnel.email])



# @receiver(post_save, sender=models.Demande)
# def sendEmailAddReponseDemande(sender, created,instance, **kwargs):
#     """Signal d'envoi d'email au demandeur des congés si sa demande a été modifié après une réponse"""
#     if not created:
#         sujet=f"Changement de la Réponse de votre demande de congé"
#         message=f"Salut, Vous recevez ce message parce que la réponse à votre demande de congé a été modifiée : {instance.conge.nature}.\Veuillez vous connecter sur le site pour plus de des détails.\nMerci Cordialement"
#         send_mail(sujet, message,"", [instance.conge.personnel.email])
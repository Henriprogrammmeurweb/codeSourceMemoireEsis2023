from django.urls import path
from .import views


urlpatterns=[
    path('conge-user', views.CongeUser, name="CongeUser"),
    path('ajout-conge', views.ajoutConge, name="ajoutConge"),
    path('detail/<str:id>/conge', views.detailConge,name="detailConge"),
    path('modif/<str:id>/conge', views.modifConge, name="modifConge"),
    path('supp/<str:id>/csonge', views.suppConge, name='suppConge'),
    path('conge-attente', views.congeAttente, name='congeAttente'),
    path('approuve-rejet-conge', views.approuveRejetConge, name="approuveRejetConge"),
    path('confirm-retour-conge', views.confirmRetourConge,name="confirmRetourConge"),
    path('conge-approuve', views.congeApprouve, name="congeApprouve"),
    path('conge-rejet', views.congeRejet, name="congeRejet"),
    path('conge-encours', views.congeEncours, name='congeEncours'),
    path('conge-attente-user', views.congeAttenteUser, name="congeAttenteUser"),
    path('liste-approbation-rejet', views.listeApprobationRejet, name="listeApprobationRejet"),
    path('modif-approbation/<str:id>/rejet', views.modifApprobationRejet, name='modifApprobationRejet'),
    path('supp/<str:id>/demande', views.suppDemande, name="suppDemande"),
    path('detail/<str:id>/demande', views.detailDemande, name="detailDemande"),
    path('consulter-conge-encours', views.consulterCongeEncours, name="consulterCongeEncours"),
    path('send-email', views.sendEmail, name='sendEmail')
]
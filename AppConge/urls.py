from django.urls import path
from .import views


urlpatterns=[
    path('conge-user', views.CongeUser, name="CongeUser"),
    path('ajout-conge', views.ajoutConge, name="ajoutConge"),
    path('detailConge=<str:id>', views.detailConge,name="detailConge"),
    path('modifConge=<str:id>', views.modifConge, name="modifConge"),
    path('suppConge=<int:id>', views.suppConge, name='suppConge'),
    path('conge-attente', views.congeAttente, name='congeAttente'),
    path('approuve-rejet-conge', views.approuveRejetConge, name="approuveRejetConge"),
    path('conge-approuve', views.congeApprouve, name="congeApprouve"),
    path('conge-rejet', views.congeRejet, name="congeRejet"),
    path('conge-encours', views.congeEncours, name='congeEncours'),
    path('conge-attente-user', views.congeAttenteUser, name="congeAttenteUser"),
    path('liste-approbation-rejet', views.listeApprobationRejet, name="listeApprobationRejet"),
    path('modifApprobationRejet=<str:id>', views.modifApprobationRejet, name='modifApprobationRejet'),
    path('suppDemande=<str:id>', views.suppDemande, name="suppDemande"),
    path('detailDemande=<str:id>', views.detailDemande, name="detailDemande"),
    path('consulter-conge-encours', views.consulterCongeEncours, name="consulterCongeEncours"),
    path('detailCongeApprobateur=<str:id>', views.detailCongeApprobateur, name="detailCongeApprobateur"),
    path('send-email', views.sendEmail, name='sendEmail')
]
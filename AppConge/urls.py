from django.urls import path
from .import views


urlpatterns=[
    path('conge-user', views.CongeUser, name="CongeUser"),
    path('ajout-conge', views.ajoutConge, name="ajoutConge"),
    path('detail/<str:id>/Conge', views.detailConge,name="detailConge"),
    path('modif/<str:id>/Conge', views.modifConge, name="modifConge"),
    path('supp/<str:id>/Conge', views.suppConge, name='suppConge'),
    path('congeAttente', views.congeAttente, name='congeAttente'),
    path('approuveRejetConge', views.approuveRejetConge, name="approuveRejetConge"),
    path('confirmRetourConge', views.confirmRetourConge,name="confirmRetourConge"),
    path('congeApprouve', views.congeApprouve, name="congeApprouve"),
    path('congeRejet', views.congeRejet, name="congeRejet"),
    path('congeEncours', views.congeEncours, name='congeEncours'),
    path('congeAttenteUser', views.congeAttenteUser, name="congeAttenteUser")
]
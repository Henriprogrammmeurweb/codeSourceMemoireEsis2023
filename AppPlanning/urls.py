from django.urls import path
from .import views


urlpatterns=[
    path("liste-planning", views.listePlanning, name="listePlanning"),
    path('ajout-planning', views.ajoutPlanning,name="ajoutPlanning"),
    path('modif/<str:id>/planning', views.modifPlanning, name="modifPlanning"),
    path('supp/<str:id>/planning', views.suppPlanning,name="suppPlanning"),
    path('liste-annee', views.listeAnnee, name='listeAnnee'),
    path('ajout-annee', views.ajoutAnnee, name="ajoutAnnee"),
    path('modif/<str:id>/annee', views.modifAnnee, name="modifAnnee"),
    path('supp/<str:id>/annee', views.suppAnnee, name='suppAnnee'),
    path('planning/<str:id>/annee', views.planningAnnee, name='planningAnnee')
]
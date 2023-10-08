from django.urls import path
from .import views


urlpatterns=[
    path("liste-planning", views.listePlanning, name="listePlanning"),
    path('ajout-planning', views.ajoutPlanning,name="ajoutPlanning"),
    path('modif/<str:id>/Planning', views.modifPlanning, name="modifPlanning"),
    path('supp/<str:id>/Planning', views.suppPlanning,name="suppPlanning"),
    path('liste-annee', views.listeAnnee, name='listeAnnee'),
    path('ajout-annee', views.ajoutAnnee, name="ajoutAnnee"),
    path('modif/<str:id>/Annee', views.modifAnnee, name="modifAnnee"),
    path('supp/<str:id>/Annee', views.suppAnnee, name='suppAnnee'),
    path('planning/<str:id>/Annee', views.planningAnnee, name='planningAnnee')
]
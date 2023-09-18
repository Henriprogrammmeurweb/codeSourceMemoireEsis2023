from django.urls import path
from .import views


urlpatterns=[
    path('dashboard', views.dashboard, name="dashboard"),
    path('liste-service', views.listeService, name="listeService"),
    path('ajout-service', views.ajoutService,name="ajoutService"),
    path('modif/<str:id>/service', views.modifService, name="modifService"),
    path('supp/<str:id>/Service', views.suppService, name="suppService"),
    path('listePersonnel/<str:id>/Service', views.listePersonnelService,name="listePersonnelService"),
    path('listePersonnel', views.listePersonnel, name="listePersonnel"),
    path('ajout-personnel', views.ajoutPersonnel, name='ajoutPersonnel'),
    path('detail/<str:id>/Personnel', views.detailPersonnel, name="detailPersonnel"),
    path('modif/<str:id>/Personnel', views.modifPersonnel, name="modifPersonnel"),
    path('supp/<str:id>/Personnel',views.suppPersonnel, name="suppPersonnel"),
    path('listeFonction', views.listeFonction, name="listeFonction"),
    path('ajoutFonction', views.ajoutFonction, name="ajoutFonction"),
    path('modif/<str:id>/Fonction',views.modifFonction, name="modifFonction"),
    path('supp/<str:id>/Fonction',views.suppFonction, name='suppFonction'),
    path('listePersonnel/<str:id>/Fonction',views.listePersonnelFonction, name="listePersonnelFonction"),
    path('listeGrade',views.listeGrade, name='listeGrade'),
    path('ajoutGrade',views.ajoutGrade, name="ajoutGrade"),
    path('supp/<str:id>/Grade',views.suppGrade, name="suppGrade"),
    path('modif/<str:id>/Grade', views.modifGrade, name="modifGrade")
]
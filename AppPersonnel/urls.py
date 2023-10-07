from django.urls import path
from .import views


urlpatterns=[
    path('dashboard', views.dashboard, name="dashboard"),
    path('liste-service', views.listeService, name="listeService"),
    path('ajout-service', views.ajoutService,name="ajoutService"),
    path('modif/<str:id>/service', views.modifService, name="modifService"),
    path('supp/<str:id>/service', views.suppService, name="suppService"),
    path('liste-personnel/<str:id>/service', views.listePersonnelService,name="listePersonnelService"),
    path('liste-personnel', views.listePersonnel, name="listePersonnel"),
    path('ajout-personnel', views.ajoutPersonnel, name='ajoutPersonnel'),
    path('detail/<str:id>/personnel', views.detailPersonnel, name="detailPersonnel"),
    path('modif/<str:id>/personnel', views.modifPersonnel, name="modifPersonnel"),
    path('supp/<str:id>/personnel',views.suppPersonnel, name="suppPersonnel"),
    path('liste-fonction', views.listeFonction, name="listeFonction"),
    path('ajout-fonction', views.ajoutFonction, name="ajoutFonction"),
    path('modif/<str:id>/fonction',views.modifFonction, name="modifFonction"),
    path('supp/<str:id>/fonction',views.suppFonction, name='suppFonction'),
    path('liste-personnel/<str:id>/fonction',views.listePersonnelFonction, name="listePersonnelFonction"),
    path('liste-grade',views.listeGrade, name='listeGrade'),
    path('ajout-grade',views.ajoutGrade, name="ajoutGrade"),
    path('supp/<str:id>/grade',views.suppGrade, name="suppGrade"),
    path('modif/<str:id>/grade', views.modifGrade, name="modifGrade")
]
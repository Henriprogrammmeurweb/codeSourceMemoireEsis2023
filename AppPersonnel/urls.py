from django.urls import path
from .import views


urlpatterns=[
    path('dashboard', views.dashboard, name="dashboard"),
    path('liste-service', views.listeService, name="listeService"),
    path('ajout-service', views.ajoutService,name="ajoutService"),
    path('modifservice=<str:id>', views.modifService, name="modifService"),
    path('suppService=<str:id>', views.suppService, name="suppService"),
    path('listePersonnelService=<str:id>', views.listePersonnelService,name="listePersonnelService"),
    path('liste-personnel', views.listePersonnel, name="listePersonnel"),
    path('ajout-personnel', views.ajoutPersonnel, name='ajoutPersonnel'),
    path('detailPersonnel=<str:id>', views.detailPersonnel, name="detailPersonnel"),
    path('modifPersonnel=<str:id>', views.modifPersonnel, name="modifPersonnel"),
    path('suppPersonnel=<str:id>',views.suppPersonnel, name="suppPersonnel"),
    path('liste-fonction', views.listeFonction, name="listeFonction"),
    path('ajout-fonction', views.ajoutFonction, name="ajoutFonction"),
    path('modifFonction=<str:id>',views.modifFonction, name="modifFonction"),
    path('suppFonction=<str:id>',views.suppFonction, name='suppFonction'),
    path('listePersonnelFonction=<str:id>',views.listePersonnelFonction, name="listePersonnelFonction"),
    path('liste-grade',views.listeGrade, name='listeGrade'),
    path('ajout-grade',views.ajoutGrade, name="ajoutGrade"),
    path('suppGrade=<str:id>',views.suppGrade, name="suppGrade"),
    path('modifGrade=<str:id>', views.modifGrade, name="modifGrade")
]
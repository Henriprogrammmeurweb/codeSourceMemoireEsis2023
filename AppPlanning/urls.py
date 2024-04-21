from django.urls import path
from .import views


urlpatterns=[
    path("liste-planning", views.listePlanning, name="listePlanning"),
    path('planningUser=<str:id>', views.planningUser, name="planningUser"),
    path('ajout-planning', views.ajoutPlanning,name="ajoutPlanning"),
    path('modifPlanning=<str:id>', views.modifPlanning, name="modifPlanning"),
    path('suppPlanning=<str:id>', views.suppPlanning,name="suppPlanning"),
    path('liste-annee', views.listeAnnee, name='listeAnnee'),
    path('ajout-annee', views.ajoutAnnee, name="ajoutAnnee"),
    path('modifAnnee=<str:id>', views.modifAnnee, name="modifAnnee"),
    path('suppAnnee=<str:id>', views.suppAnnee, name='suppAnnee'),
    path('planningAnnee=<str:id>', views.planningAnnee, name='planningAnnee'),
    path('planning-one-user', views.planningOneUser, name="planningOneUser"),
    path('planning-anuel-service', views.PlanningAnuelService, name='PlanningAnuelService'),
    path('detail-planning-annuel-service/<str:id_service>/<str:id_annee>', views.detailPlanningAnnuelService, name='detailPlanningAnnuelService'),
    path('stat-conge-service-annee', views.StatCongeServiceAnnee, name="StatCongeServiceAnnee"),
    path('detail-stat-service-annee/<str:id_service>/<str:annee>', views.detailStatServiceAnnee, name='detailStatServiceAnnee'),
    path('export_csv_conge_service/<str:id_service>/<str:annee>', views.export_csv_conge_service, name="export_csv_conge_service"),
    path('stat-planning-service-annee', views.stat_planning_service_annee, name="stat-planning-service-annee"),
    path('stat-planning-trimestre', views.stat_planning_trimestre, name="stat_planning_trimestre"),
    path('export-csv-stat-planning-trimestre/<str:annee>/<str:trimestre_debut>/<str:trimestre_fin>', views.export_csv_stat_planning_trimestre, name='export_csv_stat_planning_trimestre'),
    

    #---------------RAPPORT-----------------
    path('pdf-planning/<str:id>/annee', views.PDFplanningAnnee, name="planning-annee"),
    path('export_csv_planningAnuel=<str:id>', views.export_csv_planningAnuel, name="export_csv_planningAnuel"),
]
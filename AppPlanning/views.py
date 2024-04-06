import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.db.models import Sum, Count, Max,Min, Q
from django.urls import reverse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required, permission_required
from AppConge.models import Conge, Demande
from .import models
from django.contrib import messages
from AppAccount.models import Personnel
from AppPersonnel.models import Service, Fonction
from .import forms
import sweetify


@login_required
@permission_required("AppPlanning.view_planning", raise_exception=True)
def listePlanning(request):
    """Liste des Planification des Congés des Personnels par service"""
    liste_object=models.Planning.objects.filter(service__fonction__personnel=request.user)

    context={
            "liste_object":liste_object
        }
    return render(request, "planning/listePlanning.html",context)

@login_required
@permission_required("AppPlanning.view_planning", raise_exception=True)
def planningUser(request, id):
    """Lite des Planifications des Congés pour chaque Personnels"""
    get_id=models.Annee.objects.get(id=id)
    liste_object=models.Planning.objects.filter(annee=get_id, service__fonction__personnel=request.user)
    context={
            "liste_object":liste_object,
            "get_id":get_id
        }
    return render(request, "planning/planningUser.html",context)


@login_required
@permission_required('AppPlanning.add_planning', raise_exception=True)
def ajoutPlanning(request):
    """Insertion des planifications des Congés des Personnels"""
    fonction_user=Fonction.objects.filter(personnel=request.user)
    if len(fonction_user) == 0:
        return render(request, "error/page_403.html")
    form=forms.FormAjoutPlanningConge(request=request)
    if request.method == "POST":
        form=forms.FormAjoutPlanningConge(request.POST, request=request)
        if form.is_valid():
            personnel=form.cleaned_data['personnel']
            annee=form.cleaned_data['annee']
            date_debut=form.cleaned_data['date_debut']
            date_fin=form.cleaned_data['date_fin']
            testePlanningPersonnel=models.Planning.objects.filter(personnel=personnel, annee=annee).exists()
            if testePlanningPersonnel:
                messages.warning(request, "Ce personnel a déjà été planfié dans cette année !")
            elif date_fin < date_debut:
                messages.warning(request, "La date de début supérieure à celle de fin !") 
            elif date_debut < annee.date_debut:
                messages.warning(request, "La date de debut est inférieure à la date de debut de cette année !")
            elif date_fin > annee.date_fin :
                messages.warning(request, "La date de fin est supérieure à la date de fin de cette année")
            else:
                form.save()
                messages.warning(request, "Planification enregistrée !")
                form=forms.FormAjoutPlanningConge(request=request)
        else:
            messages.warning(request, "Formulaire invalide !")
    else:
        form=forms.FormAjoutPlanningConge(request=request)
    return render(request, "planning/ajoutPlanning.html", {"form":form})




@login_required
@permission_required('AppPlanning.change_planning', raise_exception=True)
def modifPlanning(request,id):
    """Modification des Plannification des Congés des Personnels"""
    get_id=models.Planning.objects.get(id=id)
    fonction_user=Fonction.objects.filter(personnel=request.user)
    service_user=Service.objects.filter(fonction__personnel=request.user)
    for service in service_user:
        if len(fonction_user) == 0 or service != get_id.service or get_id.getCongePlanningFini:
            return render(request, "error/page_403.html")
    form=forms.FormModifPlanningConge(request=request, instance=get_id)
    if request.method == "POST":
        form=forms.FormModifPlanningConge(request.POST, request=request, instance=get_id)
        if form.is_valid():
            annee=form.cleaned_data['annee']
            date_debut=form.cleaned_data['date_debut']
            date_fin=form.cleaned_data['date_fin']
            personnel=form.cleaned_data['personnel']
            if date_fin < date_debut:
                messages.warning(request, "La date de début est supérieure à celle de fin !") 
            elif date_debut < annee.date_debut:
                messages.warning(request, "La date de debut est inférieure à la date de debut de cette année !")
            elif date_fin > annee.date_fin :
                messages.warning(request, "La date de fin est supérieure à la date de fin de cette année")
            else:
                form.save()
                messages.warning(request, "Planification Modifiée !")
                return redirect('listePlanning')
        else:
            messages.warning(request, "Formulaire invalide !")
    else:
        form=forms.FormModifPlanningConge(request=request, instance=get_id)
    return render(request, "planning/changePlanning.html", {"form":form})
            

@login_required
@permission_required('AppPlanning.delete_planning', raise_exception=True)
def suppPlanning(request,id):
    """Suppression des Planification des Congés"""
    get_id=models.Planning.objects.get(id=id)
    fonction_user=Fonction.objects.filter(personnel=request.user)
    service_user=Service.objects.filter(fonction__personnel=request.user)
    for service in service_user:
        if len(fonction_user) == 0 or service != get_id.service or get_id.getCongePlanningFini:
            return render(request, "error/page_403.html")
    if request.method == "POST":
        get_id.delete()
        messages.warning(request, "Planning supprimé !")
        return redirect('listePlanning')
    return render(request, "planning/suppPlanning.html", {"get_id":get_id})


@login_required
@permission_required('AppPlanning.view_annee', raise_exception=True)
def listeAnnee(request):
    """Liste des Années dans la Base de données"""
    liste_object=models.Annee.objects.all().order_by('-date_creation')
    context={
        "liste_object":liste_object
    }
    return render(request, "annee/listeAnnee.html", context)


@login_required
@permission_required('AppPlanning.add_annee', raise_exception=True)
def ajoutAnnee(request):
    """Ajout des Années dans la Base données"""
    form=forms.FormAjoutAnnee()
    if request.method == "POST":
        form=forms.FormAjoutAnnee(request.POST)
        if form.is_valid():
            date_debut=form.cleaned_data['date_debut']
            date_fin=form.cleaned_data['date_fin']
            if date_debut > date_fin :
                messages.warning(request, "Date debut supérieure à la date de fin !")
            else:
                form.save()
                messages.warning(request, "Année enregistrée avec succès !")
                form=forms.FormAjoutAnnee()
        else:
            messages.warning(request, "Formulaire invalide !")
    else:
        form=forms.FormAjoutAnnee()
    return render(request, "annee/ajoutAnnee.html",{"form":form})




@login_required
@permission_required('AppPlanning.change_annee', raise_exception=True)
def modifAnnee(request,id):
    """Modification des années dans la Base de données"""
    get_id=models.Annee.objects.get(id=id)
    annee=models.Planning.objects.filter(annee=get_id).exists()
    if annee :
        return render(request, 'error/page_403.html')
    form=forms.FormAjoutAnnee(instance=get_id)
    if request.method == "POST":
        form=forms.FormAjoutAnnee(request.POST, instance=get_id)
        if form.is_valid():
            form.save()
            messages.warning(request, "Année modifiée avec succès !")
            return redirect('listeAnnee')
        else:
            messages.warning(request, "Formulaire invalide !")
    else:
        form=forms.FormAjoutAnnee(instance=get_id)
    return render(request, "annee/modifAnnee.html",{"form":form})



@login_required
@permission_required('AppPlanning.delete_annee', raise_exception=True)
def suppAnnee(request,id):
    """Suppression des Années dans la Base de données"""
    get_id=models.Annee.objects.get(id=id)
    annee=models.Planning.objects.filter(annee=get_id).exists()
    if annee :
        return render(request, 'error/page_403.html')
    if request.method == "POST":
        get_id.delete()
        messages.warning(request, " cette Année a été supprimée !")
        return redirect('listeAnnee')
    return render(request, "annee/suppAnnee.html",{"get_id":get_id})



@login_required
@permission_required('AppPlanning.view_planning', raise_exception=True)
def planningAnnee(request, id):
    """Liste des Planifications des Congés par An"""
    get_id=models.Annee.objects.get(id=id)
    liste_object=models.Planning.objects.filter(annee=get_id, service__fonction__personnel=request.user)
    context={
        "get_id":get_id,
        'liste_object':liste_object
    }
    return render(request, "planning/planningAnnee.html", context)


@login_required
def planningOneUser(request):
    """Liste des Planifications des Congés pour chaque Personnel"""
    liste_object=models.Planning.objects.filter(personnel=request.user)
    context={
        "liste_object":liste_object
    }
    return render(request, "planning/planningOneUser.html", context)



@login_required
def PlanningAnuelService(request):
    """Cette fonction groupe les plannings des congés par années et par service et compte le nombre d'hommes et de femmes"""
    group_by_planning_conge=models.Planning.objects.values('service__id', 
                                                           'service__designation',
                                                           'annee__id', 
                                                           'annee__designation'
                                                           ).annotate(nombre__personnel=Count('personnel__id'))
    for service_and_year in group_by_planning_conge:
        plannings=models.Planning.objects.filter(service__id=service_and_year['service__id'], 
                                                 annee__id=service_and_year['annee__id'])
        service_and_year['homme']=len([ligne.personnel.sexe for ligne in plannings if ligne.personnel.sexe == "M"])
        service_and_year['femme']=len([ligne.personnel.sexe for ligne in plannings if ligne.personnel.sexe == "F"])
    context={
        "group_by_planning_conge":group_by_planning_conge
    }
    return render(request, 'annee/planningAnnuel.html', context)



@login_required
def detailPlanningAnnuelService(request, id_service, id_annee):
    """Cette fonction affiche le detail sur le planning des congés de chaque service"""
    get_service=Service.objects.get(id=id_service)
    get_annee=models.Annee.objects.get(id=id_annee)
    liste_object=models.Planning.objects.filter(service=get_service, annee=get_annee)
    context={
        'liste_object':liste_object,
        'get_service':get_service,
        'get_annee':get_annee,
    }
    return render(request, 'annee/detailPlanningAnnuelService.html', context)



@login_required
def StatCongeServiceAnnee(request):
    """Cette fonction affiche les statistiques de congé de chaque service et les compte"""
    service_agent=Conge.objects.values('personnel__fonction__service__id',
                                       'personnel__fonction__service__designation', 
                                       'date_creation__year').annotate(nombre_conge=Count('id'))
    for items in service_agent:
        conge_attente=Conge.objects.filter(personnel__fonction__service__id=items['personnel__fonction__service__id']
                                           ).exclude(id__in=Demande.objects.filter().values_list('conge__id', flat=True))
        demande_sans_reponse=Conge.objects.filter(personnel__fonction__service__id=items['personnel__fonction__service__id'], 
                                                  date_fin__lt=datetime.date.today()).exclude(id__in=Demande.objects.filter().values_list('conge__id', flat=True))
        demandes=Demande.objects.filter(conge__personnel__fonction__service__id=items['personnel__fonction__service__id'])
        conge_encours=Conge.objects.filter(id__in=[ligne.conge.id for ligne in demandes if ligne.approbation == True and ligne.conge.date_fin >= datetime.date.today()])
        items['conge_approuve'] = len([ligne.approbation for ligne in demandes if ligne.approbation == True])
        items['conge_rejet'] = len([ligne.approbation for ligne in demandes if ligne.approbation == False])
        items['conge_encours'] = len([ligne for ligne in conge_encours])
        items['conge_attente'] = len([ligne for ligne in conge_attente])
        items['demande_sans_reponse'] = len([ligne for ligne in demande_sans_reponse])
    return render(request, 'annee/StatCongeServiceAnnee.html', {"service_agent":service_agent})



@login_required
def detailStatServiceAnnee(request, id_service, annee):
    """Cette fonction affiche les details de demandes des congés pour chaque service et par année"""
    liste_object=Conge.objects.filter(personnel__fonction__service__id=id_service, date_creation__year=annee)
    context={
        "liste_object":liste_object
    }
    return render(request, 'annee/detailStatServiceAnnee.html', context)




@login_required
@permission_required("AppPlanning.view_annee")
def PDFplanningAnnee(request, id):
    """Génération des PDF de Planification des Congés par AN"""
    get_id=models.Annee.objects.get(id=id)
    liste_object=models.Planning.objects.filter(annee=get_id)
    template_path = 'annee/planning_pdf.html'
    context = {'get_id': get_id, 'liste_object':liste_object}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="PlanningAnnee.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
       html, dest=response,)
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response




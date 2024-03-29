from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required, permission_required
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




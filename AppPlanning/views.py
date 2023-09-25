from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from .import models
from AppAccount.models import Personnel
from AppPersonnel.models import Service
from .import forms
import sweetify


@login_required
@permission_required("AppPlanning.view_planning", raise_exception=True)
def listePlanning(request):
    service=Service.objects.filter(fonction__personnel=request.user)
    if service :
        for services in service:
            liste_object=models.Planning.objects.filter(service=services)
        context={
            "liste_object":liste_object
        }
        return render(request, "planning/listePlanning.html",context)
    else:
        return render(request, "planning/listePlanning.html")

@login_required
@permission_required('AppPlanning.add_planning', raise_exception=True)
def ajoutPlanning(request):
    form=forms.FormAjoutPlanningConge(request=request)
    if request.method == "POST":
        form=forms.FormAjoutPlanningConge(request.POST, request=request)
        if form.is_valid():
            personnel=form.cleaned_data['personnel']
            nature=form.cleaned_data['nature']
            annee=form.cleaned_data['annee']
            date_debut=form.cleaned_data['date_debut']
            date_fin=form.cleaned_data['date_fin']
            testeConge=models.Planning.objects.filter(personnel=personnel,nature=nature, annee=annee).exists()
            if testeConge:
                sweetify.info(request, "Ce personnel a déjà été planfié dans cette année !")
            elif date_debut < annee.date_debut:
                sweetify.info(request, "La date de debut ou de fin de ce planning est inférieure à la date de debut de cette année !")
            elif date_fin > annee.date_fin :
                sweetify.info(request, "La date de fin ou de fin de ce planning est supérieure à la date de fin de cette année")
            else:
                form.save()
                sweetify.success(request, "Planification enregistrée !")
                form=forms.FormAjoutPlanningConge(request=request)
        else:
            sweetify.error(request, "Formulaire invalide !")
    else:
        form=forms.FormAjoutPlanningConge(request=request)
    return render(request, "planning/ajoutPlanning.html", {"form":form})




@login_required
@permission_required('AppPlanning.change_planning', raise_exception=True)
def modifPlanning(request,id):
    get_id=models.Planning.objects.get(id=id)
    form=forms.FormModifPlanningConge(request=request, instance=get_id)
    if request.method == "POST":
        form=forms.FormModifPlanningConge(request.POST, request=request, instance=get_id)
        if form.is_valid():
            personnel=form.cleaned_data['personnel']
            nature=form.cleaned_data['nature']
            annee=form.cleaned_data['annee']
            date_debut=form.cleaned_data['date_debut']
            date_fin=form.cleaned_data['date_fin']
            if date_debut < annee.date_debut:
                sweetify.info(request, "La date de debut de ce planning est inférieure à la date de debut de cette année !")
            elif date_fin > annee.date_fin :
                sweetify.info(request, "La date de fin de ce planning est supérieure à la date de fin de cette année")
            else:
                form.save()
                sweetify.success(request, "Planification Modifiée !")
                return redirect('listePlanning')
        else:
            sweetify.error(request, "Formulaire invalide !")
    else:
        form=forms.FormModifPlanningConge(request=request, instance=get_id)
    return render(request, "planning/changePlanning.html", {"form":form})
            

@login_required
@permission_required('AppPlanning.delete_planning', raise_exception=True)
def suppPlanning(request,id):
    get_id=models.Planning.objects.get(id=id)
    if request.method == "POST":
        get_id.delete()
        sweetify.success(request, "Planning supprimé !")
        return redirect('listePlanning')
    return render(request, "planning/suppPlanning.html")


@login_required
@permission_required('AppPlanning.view_annee', raise_exception=True)
def listeAnnee(request):
    liste_object=models.Annee.objects.all().order_by('-date_creation')
    context={
        "liste_object":liste_object
    }
    return render(request, "annee/listeAnnee.html", context)


@login_required
@permission_required('AppPlanning.add_annee', raise_exception=True)
def ajoutAnnee(request):
    form=forms.FormAjoutAnnee()
    if request.method == "POST":
        form=forms.FormAjoutAnnee(request.POST)
        if form.is_valid():
            date_debut=form.cleaned_data['date_debut']
            date_fin=form.cleaned_data['date_fin']
            if date_debut > date_fin :
                sweetify.info(request, "Date debut supérieure à la date de fin !")
            else:
                form.save()
                sweetify.success(request, "Année enregistrée avec succès !")
                form=forms.FormAjoutAnnee()
        else:
            sweetify.error(request, "Formulaire invalide !")
    else:
        form=forms.FormAjoutAnnee()
    return render(request, "annee/ajoutAnnee.html",{"form":form})




@login_required
@permission_required('AppPlanning.change_annee', raise_exception=True)
def modifAnnee(request,id):
    get_id=models.Annee.objects.get(id=id)
    annee=models.Planning.objects.filter(annee=get_id).exists()
    if annee :
        return render(request, 'error/page_403.html')
    form=forms.FormAjoutAnnee(instance=get_id)
    if request.method == "POST":
        form=forms.FormAjoutAnnee(request.POST, instance=get_id)
        if form.is_valid():
            form.save()
            sweetify.success(request, "Année modifiée avec succès !")
            return redirect('listeAnnee')
        else:
            sweetify.error(request, "Formulaire invalide !")
    else:
        form=forms.FormAjoutAnnee(instance=get_id)
    return render(request, "annee/modifAnnee.html",{"form":form})



@login_required
@permission_required('AppPlanning.delete_annee', raise_exception=True)
def suppAnnee(request,id):
    get_id=models.Annee.objects.get(id=id)
    annee=models.Planning.objects.filter(annee=get_id).exists()
    if annee :
        return render(request, 'error/page_403.html')
    if request.method == "POST":
        get_id.delete()
        sweetify.info(request, "Année modifiée a été supprimée !")
        return redirect('listeAnnee')
    return render(request, "annee/suppAnnee.html",{"get_id":get_id})
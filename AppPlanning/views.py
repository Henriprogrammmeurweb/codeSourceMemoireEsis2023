from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required, permission_required
from .import models
from AppAccount.models import Personnel
from AppPersonnel.models import Service, Fonction
from .import forms
import sweetify


@login_required
@permission_required("AppPlanning.view_planning", raise_exception=True)
def listePlanning(request):
    liste_object=models.Planning.objects.filter(personnel=request.user)
    liste_annee=models.Annee.objects.all().order_by('-date_creation')

    context={
            "liste_object":liste_object,
            "liste_annee":liste_annee
        }
    return render(request, "planning/listePlanning.html",context)

@login_required
@permission_required("AppPlanning.view_planning", raise_exception=True)
def planningUser(request, id):
    get_id=models.Annee.objects.get(id=id)
    liste_object=models.Planning.objects.filter(annee=get_id, personnel=request.user)
    context={
            "liste_object":liste_object,
            "get_id":get_id
        }
    return render(request, "planning/planningUser.html",context)


@login_required
@permission_required('AppPlanning.add_planning', raise_exception=True)
def ajoutPlanning(request):
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
                sweetify.info(request, "Ce personnel a déjà été planfié dans cette année !")
            elif date_debut < annee.date_debut:
                sweetify.info(request, "La date de debut ou de fin de ce planning est inférieure à la date de debut de cette année !")
            elif date_fin > annee.date_fin :
                sweetify.info(request, "La date de fin ou de fin de ce planning est supérieure à la date de fin de cette année")
            else:
                new_planning=form.save(commit=False)
                new_planning.personnel=request.user
                new_planning.save()
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
    fonction_user=Fonction.objects.filter(personnel=request.user)
    if len(fonction_user) == 0:
        return render(request, "error/page_403.html")
    form=forms.FormModifPlanningConge(request=request, instance=get_id)
    if request.method == "POST":
        form=forms.FormModifPlanningConge(request.POST, request=request, instance=get_id)
        if form.is_valid():
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
    fonction_user=Fonction.objects.filter(personnel=request.user)
    if len(fonction_user) == 0:
        return render(request, "error/page_403.html")
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



@login_required
@permission_required('AppPlanning.view_planning', raise_exception=True)
def planningAnnee(request, id):
    get_id=models.Annee.objects.get(id=id)
    liste_object=models.Planning.objects.filter(annee=get_id)
    if request.method == "GET":
        recherche=request.GET.get('recherche')
        if recherche:
            liste_object=models.Planning.objects.filter(personnel__username__icontains=recherche)
            sweetify.success(request, 'Résultats de la recheche')
            return render(request, "planning/planningAnnee.html", {"liste_object":liste_object})
    context={
        "get_id":get_id,
        'liste_object':liste_object
    }
    return render(request, "planning/planningAnnee.html", context)


def PDFplanningAnnee(request, id):
    get_id=models.Annee.objects.get(id=id)
    liste_object=models.Planning.objects.filter(annee=get_id)
    template_path = 'annee/planning_pdf.html'
    context = {'get_id': get_id, 'liste_object':liste_object}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="PlanningAnnee.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response,)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response




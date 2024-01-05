from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.core.mail import send_mail
from ProjectGestionPersonnel.settings import EMAIL_HOST
from django.contrib import messages
import datetime
from . import forms
from . import models
import datetime
from AppAccount.models import Personnel
import sweetify


@login_required
@permission_required("AppConge.view_conge", raise_exception=True)
def CongeUser(request):
    liste_object = models.Conge.objects.filter(personnel=request.user)
    context = {"liste_object": liste_object}
    return render(request, "conge/congeuser.html", context)


@login_required
@permission_required("AppConge.add_conge", raise_exception=True)
def ajoutConge(request):
    form = forms.FormAjoutConge()
    if request.method == "POST":
        form = forms.FormAjoutConge(request.POST)
        if form.is_valid():
            date_debut = form.cleaned_data["date_debut"]
            date_fin = form.cleaned_data["date_fin"]
            if date_fin < date_debut:
                messages.warning(request, "Date de fin inférieure à la date début !")
            else:
                conge = form.save(commit=False)
                conge.personnel = request.user
                conge.save()
                messages.warning(
                    request, "Votre demande de congé a été envoyé aux approbateurs"
                )
                form = forms.FormAjoutConge()
        else:
            messages.error(request, "Demande non envoyée merci de ressayer plus tard !")
    else:
        form = forms.FormAjoutConge()
    return render(request, "conge/ajoutConge.html", {"form": form})


@login_required
@permission_required("AppConge.change_conge", raise_exception=True)
def modifConge(request, id):
    get_conge = models.Conge.objects.get(id=id)
    demande = models.Demande.objects.filter(conge=get_conge).exists()
    if demande or get_conge.personnel != request.user:
        return render(request, "error/page_403.html")
    form = forms.FormAjoutConge(instance=get_conge)
    if request.method == "POST":
        form = forms.FormAjoutConge(request.POST, instance=get_conge)
        if form.is_valid():
            date_debut = form.cleaned_data["date_debut"]
            date_fin = form.cleaned_data["date_fin"]
            if date_fin < date_debut:
                messages.warning(request, "Date de fin inférieure à la date début !")
            else:
                conge = form.save(commit=False)
                conge.personnel = request.user
                conge.save()
                messages.warning(
                    request, "Votre demande de congé a été envoyé aux approbateurs"
                )
                return redirect("CongeUser")
        else:
            sweetify.error(request, "Demande non envoyée merci de ressayer plus tard !")
    else:
        form = forms.FormAjoutConge(instance=get_conge)
    return render(request, "conge/changeConge.html", {"form": form})


@login_required
@permission_required("AppConge.delete_conge", raise_exception=True)
def suppConge(request, id):
    get_conge = models.Conge.objects.get(id=id)
    demande = models.Demande.objects.filter(conge=get_conge).exists()
    if demande or get_conge.personnel != request.user:
        return render(request, "error/page_403.html")
    if request.method == "POST":
        get_conge.delete()
        messages.warning(
            request, f"Demande de conge {get_conge.titre} supprimé avec succès !"
        )
        return redirect("CongeUser")
    return render(request, "conge/confirmSupp.html", {"get_conge": get_conge})


@login_required
@permission_required("AppConge.view_conge", raise_exception=True)
def detailConge(request, id):
    get_conge = models.Conge.objects.get(id=id)
    if get_conge.personnel != request.user:
        return render(request, "error/page_403.html")
    context = {"get_conge": get_conge}
    return render(request, "conge/detailConge.html", context)


@login_required
@permission_required("AppConge.view_demande", raise_exception=True)
def congeAttente(request):
    liste_object = models.Conge.objects.exclude(
        id__in=models.Demande.objects.filter().values_list("conge__id", flat=True)
    )
    context = {"liste_object": liste_object}
    return render(request, "approbation/congeAttente.html", context)


@login_required
@permission_required("AppConge.add_demande", raise_exception=True)
def approuveRejetConge(request):
    form = forms.FormAddApprobation()
    if request.method == "POST":
        form = forms.FormAddApprobation(request.POST)
        if form.is_valid():
            form.save()
            messages.warning(
                request, "Merci d'avoir fourni une réponse à cette demande"
            )
            form = forms.FormAddApprobation()
        else:
            messages.warning(request, "Formulaire invalide !")
    else:
        form = forms.FormAddApprobation()
    return render(request, "approbation/approuveRejetConge.html", {"form": form})


@login_required
@permission_required("AppConge.view_conge", raise_exception=True)
def congeApprouve(request):
    liste_object = models.Demande.objects.filter(
        approbation=True, conge__personnel=request.user
    )
    context = {"liste_object": liste_object}
    return render(request, "conge/congeApprouve.html", context)


@login_required
@permission_required("AppConge.view_conge", raise_exception=True)
def congeRejet(request):
    liste_object = models.Demande.objects.filter(
        approbation=False, conge__personnel=request.user
    )
    context = {"liste_object": liste_object}
    return render(request, "conge/congeRejet.html", context)


@login_required
@permission_required("AppConge.view_conge", raise_exception=True)
def congeEncours(request):
    liste_object = (
        models.Demande.objects.exclude(approbation=False)
        .exclude(conge__date_fin__lt=datetime.date.today())
        .filter(conge__personnel=request.user)
    )
    context = {"liste_object": liste_object}
    return render(request, "conge/congeEncours.html", context)


@login_required
def congeAttenteUser(request):
    liste_object = models.Conge.objects.exclude(
        id__in=models.Demande.objects.filter().values_list("conge__id", flat=True)
    ).filter(personnel=request.user)
    context = {"liste_object": liste_object}
    return render(request, "conge/congeAttenteUser.html", context)


@login_required
@permission_required("AppConge.view_demande", raise_exception=True)
def listeApprobationRejet(request):
    liste_object = models.Demande.objects.all().order_by("-date_creation")
    context = {"liste_object": liste_object}
    return render(request, "approbation/listeApprobationRejet.html", context)


@login_required
@permission_required("AppConge.change_demande", raise_exception=True)
def modifApprobationRejet(request, id):
    get_id = models.Demande.objects.get(id=id)
    form = forms.FormChangeApprobation(instance=get_id)
    if request.method == "POST":
        form = forms.FormChangeApprobation(request.POST, instance=get_id)
        if form.is_valid():
            form.save()
            messages.warning(request, "Cette Réponse a été Modifiée")
            return redirect("listeApprobationRejet")
        else:
            messages.warning(request, "Formulaire invalide !")
    else:
        form = forms.FormChangeApprobation(instance=get_id)
    context = {"get_id": get_id, "form": form}
    return render(request, "approbation/modifApprobationRejet.html", context)


@login_required
@permission_required("AppConge.delete_demande", raise_exception=True)
def suppDemande(request, id):
    get_id = models.Demande.objects.get(id=id)
    if request.method == "POST":
        get_id.delete()
        messages.warning(request, "La réponse à cette demande a été supprimée !")
        return redirect("listeApprobationRejet")
    return render(request, "approbation/suppDemande.html", {"get_id": get_id})


@login_required
@permission_required("AppConge.view_demande", raise_exception=True)
def detailDemande(request, id):
    get_id = models.Demande.objects.get(id=id)
    return render(request, "approbation/detailDemande.html", {"get_id": get_id})


@login_required
@permission_required("AppConge.view_demande", raise_exception=True)
def consulterCongeEncours(request):
    liste_object = models.Demande.objects.exclude(approbation=False).exclude(
        conge__date_fin__lt=datetime.date.today()
    )
    context = {"liste_object": liste_object}
    return render(request, "conge/consulterCongeEncours.html", context)


@login_required
@permission_required("AppConge.view_demande", raise_exception=True)
def sendEmail(request):
    liste_demande = models.Demande.objects.exclude(
        date_fin__lt=datetime.date.today()
    ).filter(approbation=True)
    liste_user = []
    listeUserEmail = ""
    for demande in liste_demande:
        demande_user = models.Demande.objects.filter(
            date_fin__range=(demande.date_fin - datetime.timedelta(7), demande.date_fin)
        )
        for user in demande_user:
            liste_user.append(user.conge.personnel.email)
            listeUserEmail = ",".join(liste_user)
            sujet = "Fin de votre congé !!!"
            subject = f"Salut, vous recevez ce message parce que vous avez demandé un congé dernièrement.\nNous vous informons que votre congé va prendre fin dans bientôt, Merci de réprendre rapidement le Boulot comme prévu.\nPour plus des details veuillez vous connectez sur la plateforme"
            send_mail(sujet, subject, "", liste_user)
    return render(request, "alerte/finConge.html", {"listeUserEmail": listeUserEmail})

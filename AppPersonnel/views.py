import datetime
import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission
from AppConge.models import Demande, Conge
from django.contrib import messages
from AppAccount.models import Personnel
from AppPlanning.models import Planning
import sweetify
from . import forms
from . import models


@login_required
@permission_required("AppConge.view_conge", raise_exception=True)
def dashboard(request):
    """Tableau Bord des Personnels"""
    nombreConge = Conge.objects.filter(personnel=request.user).count()
    nombreApprouve = Demande.objects.filter(
        conge__personnel=request.user, approbation=True
    ).count()
    nombreRejet = Demande.objects.filter(
        conge__personnel=request.user, approbation=False
    ).count()
    nombreEncours = (
        Demande.objects.exclude(approbation=False)
        .exclude(conge__date_fin__lt=datetime.date.today())
        .filter(conge__personnel=request.user)
        .count()
    )
    nombreAttente = (
        Conge.objects.exclude(
            id__in=Demande.objects.filter().values_list("conge__id", flat=True)
        )
        .filter(personnel=request.user).exclude(date_fin__lt=datetime.date.today()).count()
    )
    plannings = Planning.objects.filter(
        service__fonction__personnel=request.user
    ).count()
    panningsUser = Planning.objects.filter(personnel=request.user).count()
    personnel = Personnel.objects.count()
    liste_object = Conge.objects.filter(personnel=request.user)[:5]
    context = {
        "nombreConge": nombreConge,
        "nombreApprouve": nombreApprouve,
        "nombreRejet": nombreRejet,
        "nombreAttente": nombreAttente,
        "nombreEncours": nombreEncours,
        "liste_object": liste_object,
        "plannings": plannings,
        "personnel": personnel,
        "panningsUser": panningsUser,
        "dateToday":datetime.date.today()
    }
    return render(request, "dashboard/dashboard.html", context)


@login_required
@permission_required("AppPersonnel.view_service", raise_exception=True)
def listeService(request):
    """Liste des Services de l'établissement"""
    liste_object = models.Service.objects.all().order_by("designation")
    context = {"liste_object": liste_object}
    return render(request, "service/listeservice.html", context)


@login_required
@permission_required("AppPersonnel.add_view", raise_exception=True)
def ajoutService(request):
    """Ajout des Services dans la base de données """
    form = forms.FormAddService()
    if request.method == "POST":
        form = forms.FormAddService(request.POST)
        if form.is_valid():
            designation = form.cleaned_data["designation"]
            verification = models.Service.objects.filter(
                designation=designation
            ).exists()
            if verification:
                messages.warning(request, f"Le service {designation} exite déjà !")
            else:
                new_service = models.Service.objects.create(designation=designation)
                new_service.save()
                messages.warning(request, f"Service {designation} crée avec succès !")
                form = forms.FormAddService()
        else:
            messages.warning(request, "Impossible d'ajouté ce Service")
    else:
        form = forms.FormAddService()
    return render(request, "service/ajoutService.html", {"form": form})


@login_required
@permission_required("AppPersonnel.add_view", raise_exception=True)
def modifService(request, id):
    """Modification des Services dans la Base de données"""
    get_id = models.Service.objects.get(id=id)
    form = forms.FormAddService(instance=get_id)
    if request.method == "POST":
        form = forms.FormAddService(request.POST, instance=get_id)
        if form.is_valid():
            designation = form.cleaned_data["designation"]
            verification = models.Service.objects.filter(
                designation=designation
            ).exists()
            if verification:
                messages.error(
                    request,
                    f"Le service {designation} exite déjà tu n'as pas apporté des Modifications!",
                )
            else:
                form.save()
                messages.success(
                    request, f"Service {get_id.designation} Modifier avec succès !"
                )
                return redirect("listeService")
        else:
            messages.error(request, "Impossible d'ajouté ce Service")
    else:
        form = forms.FormAddService(instance=get_id)
    return render(
        request, "service/modifService.html", {"form": form, "get_id": get_id}
    )


@login_required
@permission_required("AppPersonnel.delete_conge", raise_exception=True)
def suppService(request, id):
    """Suppression des Services dans la Base de données"""
    get_id = models.Service.objects.get(id=id)
    if request.method == "POST":
        try:
            get_id.delete()
            messages.warning(
                request, f"Service {get_id.designation} supprimé avec succès !"
            )
            return redirect("listeService")
        except:
            messages.warning(request, "Impossible de supprimer un objet déjà lié !")
    return render(request, "service/suppServiceConfirm.html", {"get_id": get_id})


@login_required
@permission_required("AppPersonnel.view_personnel", raise_exception=True)
def listePersonnelService(request, id):
    """Liste des Personnels par Service"""
    get_id = models.Service.objects.get(id=id)
    liste_object = Personnel.objects.filter(fonction__service=get_id)
    context = {"get_id": get_id, "liste_object": liste_object}
    return render(request, "service/listePersonnelService.html", context)


@login_required
@permission_required("AppAccount.view_personnel", raise_exception=True)
def listePersonnel(request):
    """Liste des Tous les Personnels dans la Base de Données"""
    liste_object = Personnel.objects.all().order_by("username")
    context = {"liste_object": liste_object}
    return render(request, "personnel/listePersonnel.html", context)


@login_required
@permission_required("AppAccount.view_personnel", raise_exception=True)
def detailPersonnel(request, id):
    """Detail sur les Information du Personnel"""
    get_personnel = Personnel.objects.get(id=id)
    context = {"get_personnel": get_personnel}
    return render(request, "personnel/detailPersonnel.html", context)


@login_required
@permission_required("AppAccount.add_personnel", raise_exception=True)
def ajoutPersonnel(request):
    """Creation des Comptes des Personnels dans la Base de données"""
    # Liste des permissions pour utilisateur
    ajoutConge = Permission.objects.get(codename="add_conge")
    changeConge = Permission.objects.get(codename="change_conge")
    suppConge = Permission.objects.get(codename="delete_conge")
    viewConge = Permission.objects.get(codename="view_conge")
    # -------------------------------------------------------
    ajoutPlanning = Permission.objects.get(codename="add_planning")
    changePlanning = Permission.objects.get(codename="change_planning")
    suppPlanning = Permission.objects.get(codename="delete_planning")
    viewPlanning = Permission.objects.get(codename="view_planning")
    # --------------------------------------------------------
    #
    ajoutDemande = Permission.objects.get(codename="add_demande")
    changeDemande = Permission.objects.get(codename="change_demande")
    suppDemande = Permission.objects.get(codename="delete_demande")
    viewDemande = Permission.objects.get(codename="view_demande")

    # ------------------------------------------------------------
    ajoutRetourConge = Permission.objects.get(codename="add_retour")
    changeRetourConge = Permission.objects.get(codename="change_retour")
    suppRetourConge = Permission.objects.get(codename="delete_retour")
    viewRetourConge = Permission.objects.get(codename="view_retour")

    form = forms.FormAddPersonnel()
    if request.method == "POST":
        form = forms.FormAddPersonnel(request.POST, request.FILES)
        if form.is_valid():
            matricule = form.cleaned_data["matricule"]
            email = form.cleaned_data["email"]
            username = form.cleaned_data["username"]
            postnom = form.cleaned_data["postnom"]
            prenom = form.cleaned_data["prenom"]
            sexe = form.cleaned_data["sexe"]
            grade = form.cleaned_data["grade"]
            fonction = form.cleaned_data["fonction"]
            date_naissance = form.cleaned_data["date_naissance"]
            date_engagement = form.cleaned_data["date_engagement"]
            salaire = form.cleaned_data["salaire"]
            prime = form.cleaned_data["prime"]
            etat_civil = form.cleaned_data["etat_civil"]
            password = form.cleaned_data["password"]
            is_active = form.cleaned_data["is_active"]
            is_superuser = form.cleaned_data["is_superuser"]
            demandeur = form.cleaned_data["demandeur"]
            approbateur = form.cleaned_data["approbateur"]
            consulteur = form.cleaned_data["consulteur"]
            sbgr = form.cleaned_data["sbgr"]
            planificateur = form.cleaned_data["planificateur"]
            if len(password) < 6:
                messages.warning(
                    request, "Le mot de passe doit être au moins de 6 caractère !"
                )
            elif password.isdigit():
                messages.warning(
                    request,
                    "Le mot de passe doit être composé de chiffre et de lettre !",
                )
            elif demandeur == True:
                new_personnel = Personnel.objects.create_user(
                    matricule=matricule,
                    email=email.lower(),
                    username=username,
                    postnom=postnom,
                    prenom=prenom,
                    sexe=sexe,
                    grade=grade,
                    fonction=fonction,
                    date_naissance=date_naissance,
                    date_engagement=date_engagement,
                    salaire=salaire,
                    prime=prime,
                    etat_civil=etat_civil,
                    password=password,
                    is_active=is_active,
                    is_superuser=is_superuser,
                    demandeur=demandeur,
                )
                new_personnel.user_permissions.add(ajoutConge)
                new_personnel.user_permissions.add(changeConge)
                new_personnel.user_permissions.add(viewConge)
                new_personnel.user_permissions.add(suppConge)
                new_personnel.user_permissions.add(ajoutRetourConge)
                new_personnel.user_permissions.add(changeRetourConge)
                new_personnel.user_permissions.add(suppRetourConge)
                new_personnel.user_permissions.add(viewRetourConge)
                new_personnel.save()
                messages.warning(request, "Personnel demandeur de congé crée !")
                form = forms.FormAddPersonnel()
            elif planificateur == True:
                new_personnel = Personnel.objects.create_user(
                    matricule=matricule,
                    email=email.lower(),
                    username=username,
                    postnom=postnom,
                    prenom=prenom,
                    sexe=sexe,
                    grade=grade,
                    fonction=fonction,
                    date_naissance=date_naissance,
                    date_engagement=date_engagement,
                    salaire=salaire,
                    prime=prime,
                    etat_civil=etat_civil,
                    password=password,
                    is_active=is_active,
                    is_superuser=is_superuser,
                    planificateur=planificateur,
                )
                new_personnel.user_permissions.add(ajoutConge)
                new_personnel.user_permissions.add(changeConge)
                new_personnel.user_permissions.add(viewConge)
                new_personnel.user_permissions.add(suppConge)
                new_personnel.user_permissions.add(ajoutRetourConge)
                new_personnel.user_permissions.add(changeRetourConge)
                new_personnel.user_permissions.add(suppRetourConge)
                new_personnel.user_permissions.add(viewRetourConge)
                new_personnel.user_permissions.add(ajoutPlanning)
                new_personnel.user_permissions.add(changePlanning)
                new_personnel.user_permissions.add(viewPlanning)
                new_personnel.user_permissions.add(suppPlanning)
                new_personnel.save()
                messages.warning(request, "Personnel Planificateur de congé créé !")
                form = forms.FormAddPersonnel()
            elif approbateur == True:
                new_personnel = Personnel.objects.create_user(
                    matricule=matricule,
                    email=email.lower(),
                    username=username,
                    postnom=postnom,
                    prenom=prenom,
                    sexe=sexe,
                    grade=grade,
                    fonction=fonction,
                    date_naissance=date_naissance,
                    date_engagement=date_engagement,
                    salaire=salaire,
                    prime=prime,
                    etat_civil=etat_civil,
                    password=password,
                    is_active=is_active,
                    is_superuser=is_superuser,
                    approbateur=approbateur,
                )
                new_personnel.user_permissions.add(ajoutConge)
                new_personnel.user_permissions.add(changeConge)
                new_personnel.user_permissions.add(viewConge)
                new_personnel.user_permissions.add(suppConge)
                new_personnel.user_permissions.add(ajoutRetourConge)
                new_personnel.user_permissions.add(changeRetourConge)
                new_personnel.user_permissions.add(suppRetourConge)
                new_personnel.user_permissions.add(viewRetourConge)
                new_personnel.user_permissions.add(ajoutDemande)
                new_personnel.user_permissions.add(changeDemande)
                new_personnel.user_permissions.add(viewDemande)
                new_personnel.user_permissions.add(suppDemande)
                new_personnel.save()
                messages.warning(request, "Personnel approbateur des congés créé")
                form = forms.FormAddPersonnel()
            else:
                new_personnel = Personnel.objects.create_user(
                    matricule=matricule,
                    email=email.lower(),
                    username=username,
                    postnom=postnom,
                    prenom=prenom,
                    sexe=sexe,
                    grade=grade,
                    fonction=fonction,
                    date_naissance=date_naissance,
                    date_engagement=date_engagement,
                    salaire=salaire,
                    prime=prime,
                    etat_civil=etat_civil,
                    password=password,
                    is_active=is_active,
                    is_superuser=is_superuser,
                    demandeur=demandeur,
                    approbateur=approbateur,
                    consulteur=consulteur,
                    sbgr=sbgr,
                )
                new_personnel.save()
                messages.warning(request, "Personnel ajouté avec succès !")
                form = forms.FormAddPersonnel()
        else:
            messages.warning(request, "Personnel non ajouté  !")
    else:
        form = forms.FormAddPersonnel()
    return render(request, "personnel/ajoutPersonnel.html", {"form": form})


@login_required
@permission_required("AppAccount.change_personnel", raise_exception=True)
def modifPersonnel(request, id):
    """Modification des Informations des Personels dans la Base de données"""
    get_personnel = Personnel.objects.get(id=id)
    form = forms.FormChangePersonnel(instance=get_personnel)
    if request.method == "POST":
        form = forms.FormChangePersonnel(
            request.POST, request.FILES, instance=get_personnel
        )
        if form.is_valid():
            form.save()
            messages.warning(
                request,
                f"Information de {get_personnel.getPersonnel} changée avec succès !",
            )
            return redirect("listePersonnel")
        else:
            messages.error(request, "Informations non changées !")
    else:
        form = forms.FormChangePersonnel(instance=get_personnel)
    return render(request, "personnel/modifPersonnel.html", {"form": form})


@login_required
@permission_required("AppPersonnel.delete_view", raise_exception=True)
def suppPersonnel(request, id):
    """Suppression des Personnels dans la Base de données"""
    get_personnel = Personnel.objects.get(id=id)
    if request.method == "POST":
        try:
            get_personnel.delete()
            messages.warning(
                request, f"Personnel {get_personnel.getPersonnel} supprimé !"
            )
            return redirect("listePersonnel")
        except:
            messages.warning(request, "Impossible de supprimer ce personnel !")
    context = {"get_personnel": get_personnel}
    return render(request, "personnel/confirmSuppPersonnel.html", context)


@login_required
@permission_required("AppPersonnel.view_fonction", raise_exception=True)
def listeFonction(request):
    """Liste des Fonctions qui se trouvent dans les services de l'Etablissement"""
    liste_object = models.Fonction.objects.all().order_by("-date_creation")
    context = {"liste_object": liste_object}
    return render(request, "fonction/listeFonction.html", context)


@login_required
@permission_required("AppPersonnel.add_fonction", raise_exception=True)
def ajoutFonction(request):
    """Ajout des Fontions dans la Base de données"""
    form = forms.FormAddFonction()
    if request.method == "POST":
        form = forms.FormAddFonction(request.POST)
        if form.is_valid():
            designation = form.cleaned_data["designation"]
            service = form.cleaned_data["service"]
            verification = models.Fonction.objects.filter(
                designation=designation, service=service
            ).exists()
            if verification:
                messages.warning(request, "Cette fonction existe déjà !")
            else:
                form.save()
                messages.warning(request, "Fonction enregistrée !")
                form = forms.FormAddFonction()
        else:
            messages.warning(request, "Formulaire invalide !")
    else:
        form = forms.FormAddFonction()
    return render(request, "fonction/ajoutFonction.html", {"form": form})


@login_required
@permission_required("AppPersonnel.change_fonction", raise_exception=True)
def modifFonction(request, id):
    """Modification des Fontions"""
    get_id = models.Fonction.objects.get(id=id)
    form = forms.FormEditerFonction(instance=get_id)
    if request.method == "POST":
        form = forms.FormEditerFonction(request.POST, instance=get_id)
        if form.is_valid():
            designation = form.cleaned_data["designation"]
            service = form.cleaned_data["service"]
            verification = models.Fonction.objects.filter(
                designation=designation, service=service
            ).exists()
            if verification:
                messages.warning(request, "Cette fonction existe déjà !")
            else:
                form.save()
                messages.warning(
                    request, f"La fonction {get_id.designation} a été modifiée !"
                )
                return redirect("listeFonction")
        else:
            messages.warning(request, "Formulaire invalide !")
    else:
        get_id = models.Fonction.objects.get(id=id)
    context = {"get_id": get_id, "form": form}
    return render(request, "fonction/modifFonction.html", context)


@login_required
@permission_required("AppPersonnel.delete_fonction", raise_exception=True)
def suppFonction(request, id):
    """Suppression des Fonctions qui sont dans la Base de données"""
    get_id = models.Fonction.objects.get(id=id)
    if request.method == "POST":
        try:
            get_id.delete()
            messages.warning(
                request, f"La fonction {get_id.designation} a été supprimée !"
            )
            return redirect("listeFonction")
        except:
            messages.warning(request, "Impossible de supprimer cette Fonction !")
    return render(request, "fonction/confirmSuppFonction.html", {"get_id": get_id})


@login_required
@permission_required("AppAccount.view_personnel", raise_exception=True)
def listePersonnelFonction(request, id):
    """Liste des Personnels par Fonction"""
    get_id = models.Fonction.objects.get(id=id)
    liste_object = Personnel.objects.filter(fonction=get_id)
    context = {"get_id": get_id, "liste_object": liste_object}
    return render(request, "fonction/listePersonnelFonction.html", context)


@login_required
@permission_required("AppPeronnel.view_grade", raise_exception=True)
def listeGrade(request):
    """Liste des Grades des Personnels de l'etablissement"""
    liste_object = models.Grade.objects.all().order_by("-date_creation")
    context = {"liste_object": liste_object}
    return render(request, "grade/listeGrade.html", context)


@login_required
@permission_required("AppPersonnel.view_conge", raise_exception=True)
def ajoutGrade(request):
    """Ajout des Grades des Personnels dans la Base de données"""
    form = forms.FormAddGrade()
    if request.method == "POST":
        form = forms.FormAddGrade(request.POST)
        if form.is_valid():
            form.save()
            messages.warning(request, "Grade enregistré avec succès !")
            form = forms.FormAddGrade()
        else:
            messages.warning(request, "Formulaire invalide !")
    else:
        form = forms.FormAddGrade()
    return render(request, "grade/ajoutGrade.html", {"form": form})


@login_required
@permission_required("AppPersonnel.change_conge", raise_exception=True)
def modifGrade(request, id):
    """Modification des Grades des Personnels dans la Base de données"""
    get_id = models.Grade.objects.get(id=id)
    form = forms.FormAddGrade(instance=get_id)
    if request.method == "POST":
        form = forms.FormAddGrade(request.POST, instance=get_id)
        if form.is_valid():
            form.save()
            messages.warning(request, "Grade modifié avec succès !")
            return redirect("listeGrade")
        else:
            messages.warning(request, "Formulaire invalide !")
    return render(request, "grade/modifGrade.html", {"form": form, "get_id": get_id})


@login_required
@permission_required("AppPersonnel.delete_conge", raise_exception=True)
def suppGrade(request, id):
    """Suppression des Grades dans la Base données des données"""
    get_id = models.Grade.objects.get(id=id)
    if request.method == "POST":
        try:
            get_id.delete()
            messages.warning(request, "Grade supprimé avec succès !")
            return redirect("listeGrade")
        except:
            messages.warning(request, "Impossible de supprimer ce grade !")
    return render(request, "grade/suppGrade.html", {"get_id": get_id})


@login_required
@permission_required("AppAccount.view_personnel", raise_exception=True)
def listePersonnelGrade(request, id):
    """Liste des Personnels par Grade"""
    get_id = models.Grade.objects.get(id=id)
    liste_object = Personnel.objects.filter(grade=get_id)
    context = {"get_id": get_id, "liste_object": liste_object}
    return render(request, "grade/listePersonnelGrade.html", context)


@login_required
def export_personnel_csv(request):
    liste_personnel=Personnel.objects.all()
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="articles.csv"'
    writer=csv.writer(response)
    writer.writerow(["Nom", "Postnom", "Prenom", "Sexe", "Service", "Fonction", "Grade", "Conges Approuves", "Conges Rejetes","Demande Total"])
    liste_data=[ligne if ligne is not None else 'Null' for ligne in liste_personnel]
    for item in liste_data:
        demande_approuve=Demande.objects.filter(approbation=True, conge__personnel=item.id).count()
        demande_rejet=Demande.objects.filter(approbation=False, conge__personnel=item.id).count()
        writer.writerow([item.username, item.postnom, item.prenom, item.sexe, item.fonction, item.fonction.service, item.grade,demande_approuve, demande_rejet, item.getNombreDemandeConge])
    return response
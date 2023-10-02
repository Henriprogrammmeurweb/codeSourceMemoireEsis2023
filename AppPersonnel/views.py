from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission
from AppConge.models import Demande,Conge, Retour
from django.contrib import messages
from AppAccount.models import Personnel
import sweetify
from .import forms
from .import models

@login_required
@permission_required("AppConge.view_conge", raise_exception=True)
def dashboard(request):
    nombreConge=Conge.objects.filter(personnel=request.user).count()
    nombreApprouve=Demande.objects.filter(conge__personnel=request.user, approbation=True).count()
    nombreRejet=Demande.objects.filter(conge__personnel=request.user, approbation=False).count()
    nombreEncours=Demande.objects.exclude(approbation=False).exclude(id__in=Retour.objects.filter().values_list("demande__id",flat=True)).filter(conge__personnel=request.user).count()
    nombreAttente=Conge.objects.exclude(id__in=Demande.objects.filter().values_list('conge__id', flat=True)).filter(personnel=request.user).count()
    retourConfirme=Retour.objects.filter(demande__conge__personnel=request.user).count()
    context={
        "nombreConge":nombreConge,
        "nombreApprouve":nombreApprouve,
        "nombreRejet":nombreRejet,
        "nombreAttente":nombreAttente,
        "nombreEncours":nombreEncours,
        "retourConfirme":retourConfirme
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
@permission_required("AppPersonnel.view_service", raise_exception=True)
def listeService(request):
    liste_object=models.Service.objects.all().order_by('designation')
    if request.method == "GET":
        recherche=request.GET.get('recherche')
        if recherche:
            liste_object=models.Service.objects.filter(designation__icontains=recherche)
            sweetify.success(request, 'Résultats de la recheche')
            return render(request, "service/listeservice.html", {"liste_object":liste_object})
    context={
        "liste_object":liste_object
    }
    return render(request, "service/listeservice.html", context)

@login_required
@permission_required('AppPersonnel.add_view', raise_exception=True)
def ajoutService(request):
    form=forms.FormAddService()
    if request.method =="POST":
        form=forms.FormAddService(request.POST)
        if form.is_valid():
            designation=form.cleaned_data['designation']
            verification=models.Service.objects.filter(designation=designation).exists()
            if verification:
                sweetify.error(request, f"Le service {designation} exite déjà !")
            else:
                new_service=models.Service.objects.create(designation=designation)
                new_service.save()
                sweetify.success(request, f"Service {designation} crée avec succès !")
                form=forms.FormAddService()
        else:
            sweetify.error(request, "Impossible d'ajouté ce Service")
    else:
        form=forms.FormAddService()
    return render(request, "service/ajoutService.html",{"form":form})

@login_required
@permission_required('AppPersonnel.add_view', raise_exception=True)
def modifService(request,id):
    get_id=models.Service.objects.get(id=id)
    form=forms.FormAddService(instance=get_id)
    if request.method =="POST":
        form=forms.FormAddService(request.POST, instance=get_id)
        if form.is_valid():
            designation=form.cleaned_data['designation']
            verification=models.Service.objects.filter(designation=designation).exists()
            if verification:
                sweetify.error(request, f"Le service {designation} exite déjà tu n'as pas apporté des Modifications!")
            else:
                form.save()
                sweetify.success(request, f"Service {get_id.designation} Modifier avec succès !")
                return redirect('listeService')
        else:
            sweetify.error(request, "Impossible d'ajouté ce Service")
    else:
        form=forms.FormAddService(instance=get_id)
    return render(request, "service/modifService.html",{"form":form, "get_id":get_id})




@login_required
@permission_required("AppPersonnel.delete_conge", raise_exception=True)
def suppService(request,id):
    get_id=models.Service.objects.get(id=id)
    if request.method == "POST":
        get_id.delete()
        sweetify.success(request, f"Service {get_id.designation} supprimer avec succès !")
        return redirect('listeService')
    return render(request, 'service/suppServiceConfirm.html',{"get_id":get_id})

@login_required
@permission_required("AppPersonnel.view_personnel", raise_exception=True)
def listePersonnelService(request,id):
    get_id=models.Service.objects.get(id=id)
    liste_object=Personnel.objects.filter(fonction__service=get_id)
    context={
        "get_id":get_id,
        'liste_object':liste_object
    }
    return render(request, "service/listePersonnelService.html", context)


@login_required
@permission_required("AppAccount.view_personnel", raise_exception=True)
def listePersonnel(request):
    liste_object=Personnel.objects.all().order_by('-date_creation')
    if request.method == "GET":
        recherche=request.GET.get('recherche')
        if recherche:
            liste_object=Personnel.objects.filter(username__icontains=recherche)
            sweetify.success(request, 'Résultats de la recheche')
            return render(request, "personnel/listePersonnel.html", {"liste_object":liste_object})
    context={
        "liste_object":liste_object
    }
    return render(request, "personnel/listePersonnel.html", context)

@login_required
@permission_required('AppAccount.view_personnel', raise_exception=True)
def detailPersonnel(request,id):
    get_personnel=Personnel.objects.get(id=id)
    context={
        "get_personnel":get_personnel
    }
    return render(request, 'personnel/detailPersonnel.html', context)





@login_required
@permission_required("AppAccount.add_personnel", raise_exception=True)
def ajoutPersonnel(request):
    liste_perms=Permission.objects.all()
    form=forms.FormAddPersonnel()
    if request.method == "POST":
        form=forms.FormAddPersonnel(request.POST, request.FILES)
        if form.is_valid():
            matricule=form.cleaned_data['matricule']
            email=form.cleaned_data['email']
            username=form.cleaned_data['username']
            postnom=form.cleaned_data['postnom']
            prenom=form.cleaned_data['prenom']
            sexe=form.cleaned_data['sexe']
            grade=form.cleaned_data['grade']
            fonction=form.cleaned_data['fonction']
            date_naissance=form.cleaned_data['date_naissance']
            date_engagement=form.cleaned_data['date_engagement']
            salaire=form.cleaned_data['salaire']
            prime=form.cleaned_data['prime']
            etat_civil=form.cleaned_data['etat_civil']
            password=form.cleaned_data['password']
            is_active=form.cleaned_data['is_active']
            is_superuser=form.cleaned_data['is_superuser']
            demandeur=form.cleaned_data["demandeur"]
            approbateur=form.cleaned_data["approbateur"]
            consulteur=form.cleaned_data["consulteur"]
            sbgr=form.cleaned_data['sbgr']
            new_personnel=Personnel.objects.create_user(matricule=matricule, email=email.lower(), username=username,postnom=postnom,prenom=prenom,
                                                        sexe=sexe, grade=grade, fonction=fonction, date_naissance=date_naissance, date_engagement=date_engagement,
                                                        salaire=salaire,prime=prime,etat_civil=etat_civil,password=password,is_active=is_active,is_superuser=is_superuser,
                                                        demandeur=demandeur, approbateur=approbateur, consulteur=consulteur, sbgr=sbgr)
            new_personnel.save()
            sweetify.success(request, "Personnel ajouté avec succès !")
            form=forms.FormAddPersonnel()
        else:
            sweetify.error(request, "Personnel non ajouté  !")
    else:
        form=forms.FormAddPersonnel()
    return render(request, "personnel/ajoutPersonnel.html",{"form":form})

@login_required
@permission_required('AppAccount.change_personnel', raise_exception=True)
def modifPersonnel(request,id):
    get_personnel=Personnel.objects.get(id=id)
    form=forms.FormChangePersonnel(instance=get_personnel)
    if request.method == "POST" :
        form=forms.FormChangePersonnel(request.POST, request.FILES,instance=get_personnel)
        if form.is_valid():
            form.save()
            sweetify.success(request, "Information d'un Personnel changée avec succès !")
            return redirect('listePersonnel')
        else:
            sweetify.error(request,"Informations non changées !")
    else:
        form=forms.FormChangePersonnel(instance=get_personnel)
    return render(request, "personnel/modifPersonnel.html",{"form":form})


@login_required
@permission_required('AppPersonnel.delete_view', raise_exception=True)
def suppPersonnel(request,id):
    get_personnel=Personnel.objects.get(id=id)
    if request.method == "POST":
        get_personnel.delete()
        sweetify.success(request, f"Personnel {get_personnel.username}-{get_personnel.postnom} supprimé !" )
        return redirect('listePersonnel')
    context={
        "get_personnel":get_personnel
    }
    return render(request, 'personnel/confirmSuppPersonnel.html',context)


@login_required
@permission_required("AppPersonnel.view_fonction", raise_exception=True)
def listeFonction(request):
    liste_object=models.Fonction.objects.all().order_by('-date_creation')
    if request.method == "GET":
        recherche=request.GET.get('recherche')
        if recherche:
            liste_object=models.Fonction.objects.filter(designation__icontains=recherche)
            sweetify.success(request, 'Résultats de la recheche')
            return render(request, "fonction/listeFonction.html", {"liste_object":liste_object})
    context={
        "liste_object":liste_object
    }
    return render(request, 'fonction/listeFonction.html', context)


@login_required
@permission_required("AppPersonnel.add_fonction",raise_exception=True)
def ajoutFonction(request):
    form=forms.FormAddFonction()
    if request.method == "POST":
        form=forms.FormAddFonction(request.POST)
        if form.is_valid():
            designation=form.cleaned_data['designation']
            verification=models.Fonction.objects.filter(designation=designation).exists()
            if verification:
                sweetify.info(request, "Cette fonction existe déjà !")
            else:
                form.save()
                sweetify.success(request, "Fonction enregistrée !")
                form=forms.FormAddFonction()
        else:
            sweetify.error(request, "Formulaire invalide !")
    else:
        form=forms.FormAddFonction()
    return render(request, "fonction/ajoutFonction.html",{"form":form})



@login_required
@permission_required("AppPersonnel.change_fonction",raise_exception=True)
def modifFonction(request,id):
    get_id=models.Fonction.objects.get(id=id)
    form=forms.FormEditerFonction(instance=get_id)
    if request.method == "POST" :
        form=forms.FormEditerFonction(request.POST,instance=get_id)
        if form.is_valid():
            form.save()
            sweetify.success(request, f"La fonction {get_id.designation} a été modifiée !")
            return redirect('listeFonction')
        else:
            sweetify.error(request, "Formulaire invalide !")
    else:
        get_id=models.Fonction.objects.get(id=id)
    context={
        "get_id":get_id,
        'form':form
    }
    return render(request, "fonction/modifFonction.html", context)

@login_required
@permission_required("AppPersonnel.delete_fonction",raise_exception=True)
def suppFonction(request,id):
    get_id=models.Fonction.objects.get(id=id)
    if request.method == "POST":
        get_id.delete()
        sweetify.info(request, f"La fonction {get_id.designation} a été supprimée !")
        return redirect('listeFonction')
    return render(request, "fonction/confirmSuppFonction.html",{"get_id":get_id})


@login_required
@permission_required("AppAccount.view_personnel",raise_exception=True)
def listePersonnelFonction(request,id):
    get_id=models.Fonction.objects.get(id=id)
    liste_object=Personnel.objects.filter(fonction=get_id)
    context={
        "get_id":get_id,
        'liste_object':liste_object
    }
    return render(request, "fonction/listePersonnelFonction.html",context)


@login_required
@permission_required("AppPeronnel.view_grade",raise_exception=True)
def listeGrade(request):
    liste_object=models.Grade.objects.all().order_by('-date_creation')
    if request.method == "GET":
        recherche=request.GET.get('recherche')
        if recherche:
            liste_object=models.Grade.objects.filter(designation__icontains=recherche)
            sweetify.success(request, 'Résultats de la recheche')
            return render(request, "grade/listeGrade.html", {"liste_object":liste_object})
    context={
        "liste_object":liste_object
    }
    return render(request, "grade/listeGrade.html",context)

@login_required
@permission_required("AppPersonnel.view_conge",raise_exception=True)
def ajoutGrade(request):
    form=forms.FormAddGrade()
    if request.method == "POST":
        form=forms.FormAddGrade(request.POST)
        if form.is_valid():
            form.save()
            sweetify.success(request, "Grade enregistré avec succès !")
            form=forms.FormAddGrade()
        else:
            sweetify.error(request, "Formulaire invalide !")
    else:
        form=forms.FormAddGrade()
    return render(request, "grade/ajoutGrade.html",{"form":form})


@login_required
@permission_required("AppPersonnel.change_conge",raise_exception=True)
def modifGrade(request,id):
    get_id=models.Grade.objects.get(id=id)
    form=forms.FormAddGrade(instance=get_id)
    if request.method == "POST":
        form=forms.FormAddGrade(request.POST,instance=get_id)
        if form.is_valid():
            form.save()
            sweetify.info(request, "Grade modifié avec succès !")
            return redirect('listeGrade')
        else:
            sweetify.error(request, 'Formulaire invalide !')
    return render(request, 'grade/modifGrade.html',{"form":form,"get_id":get_id})




@login_required
@permission_required("AppPersonnel.delete_conge",raise_exception=True)
def suppGrade(request,id):
    get_id=models.Grade.objects.get(id=id)
    if request.method == "POST":
        get_id.delete()
        sweetify.info(request, "Grade supprimé avec succès !")
        return redirect('listeGrade')
    return render(request, "grade/suppGrade.html",{"get_id":get_id})
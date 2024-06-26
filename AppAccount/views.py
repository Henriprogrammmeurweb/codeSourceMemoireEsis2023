from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .import models
import sweetify
from .import forms




def loginUser(request):
    """Connexion de l'utilisateur au système """
    if request.user.is_authenticated :
        return redirect('dashboard')
    form=forms.FormLogin()
    if request.method == "POST":
        form=forms.FormLogin(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            user=authenticate(email=email, password=password)
            if not "@" in email:
                messages.warning(request, "Adresse Email incorrect")
            elif user:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Authentification échouée Merci de ressayer !")
        else:
            messages.error(request, "Oups ! Formulaire invalide")
    else:
        form=forms.FormLogin()
    return render(request, "login/login.html",{"form":form})

@login_required
def logoutUser(request):
    """Deconnexion du Personnel"""
    logout(request)
    messages.info(request, "Vous êtes déconnecté !")
    return redirect('index')

def page403(request, exception):
    """Page 403 personnalisée permissions requises"""
    return render(request, "error/page_403.html")


def page404(request, exception):
    """Page 404 personnalisé page introuvable !"""
    return render(request, "error/page_404.html")

def page500(request):
    """Page 500 Personnalisé erreur du Serveur"""
    return render(request, "error/page_500.html")


@login_required
def changePassword(request):
    """Changement du Mot de passe du Personnel"""
    form=forms.FormChangePassword(request.user)
    if request.method == "POST":
        form=forms.FormChangePassword(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "Vous êtes maintenant deconnecté, votre mot de passe a été changé, connectez-vous à nouveau !")
            return redirect('index')
        else:
            messages.error(request, "Formulaire invalide, veuillez renseigner les champs correctement !")
    else:
        form=forms.FormChangePassword(request.user)
    return render(request, "password/passwordchange.html",{"form":form})



def appropos(request):
    """Appropos de l'éblissement"""
    return render(request, "appropos/appropos.html")

def contact(request):
    """Page des Contacts"""
    form=forms.FormContact()
    return render(request, "contact.html", {"form":form})


@login_required
def ProfilUser(request):
    """Profil du personnel/Informations"""
    return render(request, "profil/profilUser.html")

@login_required
def ChangeProfil(request, id):
    """Changement ou suppression du Profil/Photo du personnel"""
    get_user=models.Personnel.objects.get(id=id)
    if get_user != request.user:
        return render(request,"error/page_403.html")
    form=forms.ChangeProfilUser(instance=get_user)
    if request.method == "POST":
        form=forms.ChangeProfilUser(request.POST, request.FILES, instance=get_user)
        if form.is_valid():
            form.save()
            messages.warning(request, "Votre photo a été mise à jour !")
            return redirect('ProfilUser')
        else:
            messages.warning(request, "Impossible de modifier votre photo")
    else:
        form=forms.ChangeProfilUser(instance=get_user)
    context={
        "get_user":get_user,
        'form':form
    }
    return render(request, "profil/changeProfil.html", context)

@login_required
def guideUser(request):
    """Guide d'utilisation descriptif du site !"""
    return render(request, "guide/guideUser.html")
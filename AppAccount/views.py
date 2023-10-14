from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
import sweetify
from .import forms


def index(request):
    return render(request, 'index/index.html')

def loginUser(request):
    if request.user.is_authenticated :
        return redirect('dashboard')
    form=forms.FormLogin()
    if request.method == "POST":
        form=forms.FormLogin(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            user=authenticate(email=email, password=password)
            if user:
                login(request, user)
                if request.user.approbateur :
                    return redirect('congeAttente')
                elif request.user.is_superuser or request.user.sbgr:
                    return redirect('listePersonnel')
                else:
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
    logout(request)
    messages.info(request, "Vous êtes déconnecté !")
    return redirect('loginUser')

def page403(request, exception):
    return render(request, "error/page_403.html")


def page404(request, exception):
    return render(request, "error/page_404.html")

def page500(request):
    return render(request, "error/page_500.html")


@login_required
def changePassword(request):
    form=forms.FormChangePassword(request.user)
    if request.method == "POST":
        form=forms.FormChangePassword(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "Vous êtes maintenant deconnecté, votre mot de passe a été changé, connectez-vous à nouveau !")
            return redirect('loginUser')
        else:
            sweetify.error(request, "Impossible !")
    else:
        form=forms.FormChangePassword(request.user)
    return render(request, "password/passwordchange.html",{"form":form})



def appropos(request):
    return render(request, "appropos.html")




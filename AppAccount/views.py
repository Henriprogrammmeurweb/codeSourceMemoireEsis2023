from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .import forms


def index(request):
    return render(request, 'index/index.html')

def loginUser(request):
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
    return redirect('loginUser')

def page403(request, exception):
    return render(request, "error/page_403.html")


def page404(request, exception):
    return render(request, "error/page_404.html")

def page500(request):
    return render(request, "error/page_500.html")
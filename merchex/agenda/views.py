from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from agenda.models import Medecin

# Create your views here.

def home(request):
    return render(request, "logs/index.html")

def signup(request):

    if request.method == "POST":

        username = request.POST['nom']
        email = request.POST['mail']
        mdp = request.POST['motdepasse']

        myuser = Medecin.objects.create_user(username=username, email=email,password = mdp)

        myuser.tel = request.POST['telephone']
        myuser.first_name = request.POST['prenom']
        myuser.last_name = request.POST['nom']

        myuser.save()

        messages.success(request, "Utilisateur enregistré.")

        return redirect('signin')




    return render(request, "logs/signup.html")

def signin(request):

    if request.method == "POST":

        username = request.POST['nom']
        mdp = request.POST['motdepasse']

        user = authenticate(username = username, password = mdp)

        if user is not None:
            login(request, user)
            prenom = user.first_name
            return render(request, "logs/index.html", {prenom: prenom})
        
        else:
            messages.error(request, "Mauvais identifiants")
            return redirect('home')


    return render(request, "logs/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Déconnexion réussie !")
    return redirect('home')
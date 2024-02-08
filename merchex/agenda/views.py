import datetime
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from agenda.models import Medecin
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token
from merchex import settings
from django.contrib.auth import get_user_model


User = get_user_model()

# Create your views here.

def home(request):
    return render(request, "logs/index.html")

def signup(request):

    if request.method == "POST":

        username = request.POST['nom']
        email = request.POST['mail']
        mdp = request.POST['motdepasse']
        mdp2 = request.POST['confirmationmotdepasse']

        # if User.objects.filter(email=email):
        #     messages.error(request, "Adresse email déjà utilisée ! Réessayez.")
        #     return redirect('home')

        if mdp != mdp2:
            messages.error(request, "Les mots de passe ne correspondent pas.")


        myuser = Medecin.objects.create_user(username=username, email=email,password = mdp)

        myuser.tel = request.POST['telephone']
        myuser.first_name = request.POST['prenom']
        myuser.last_name = request.POST['nom']
        myuser.is_active = False
        myuser.save()

        messages.success(request, "Utilisateur enregistré. Nous vous avons envoyé un email de confirmation. Veuillez activer votre compte !")

        #Email confirmation
        current_site = get_current_site(request)
        email_subject = "Confirm your email - P24 Agenda"
        message = render_to_string("logs/email_confirmation.html", {
            "name": myuser.first_name, 
            "domain": current_site.domain, 
            "uid": urlsafe_base64_encode(force_bytes(myuser.pk)),
            "token": generate_token.make_token(myuser)
            })
        
        email = EmailMessage(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )

        email.fail_silently = True
        email.send()

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
            return render(request, "accueil/weekly.html", {prenom: prenom})
        
        else:
            messages.error(request, "Mauvais identifiants")
            return redirect('home')


    return render(request, "logs/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Déconnexion réussie !")
    return redirect('home')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError,User.DoesNotExist):
        
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Votre compte a été activé avec succès !")
        return redirect('signin')
    else:
        return render(request, 'logs/activation_fail.html')
    

def compte(request):
    #ICI, on récupère tous les patients du médecin connecté
    patient = ["Alexandre","Dupont", 3, "23 janvier 2024"] #Juste un exemple
    patients = [patient, patient]
    return render(request, 'moncompte/compte.html', {'patients': patients})

def agenda(request):
    
    return render(request, "accueil/weekly.html")

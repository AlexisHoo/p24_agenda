import datetime
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from agenda.models import Medecin, CustomUser, Patient
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token
from merchex import settings
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from .forms import PatientForm, CustomUserForm


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
        first_name = request.POST['prenom']
        last_name = request.POST['nom']

        # if User.objects.filter(email=email):
        #     messages.error(request, "Adresse email déjà utilisée ! Réessayez.")
        #     return redirect('home')

        if mdp != mdp2:
            messages.error(request, "Les mots de passe ne correspondent pas.")

        myuser = CustomUser.objects.create(username=username, email=email, first_name = first_name, last_name = last_name, is_active = True, is_medecin = True)
        myuser.set_password(mdp)
        myuser.save()
        
        tel = request.POST['telephone']
        medecin = Medecin.objects.create(user = myuser, tel_medecin = tel)
        medecin.save()
  


        messages.success(request, "Utilisateur enregistré. Nous vous avons envoyé un email de confirmation. Veuillez activer votre compte !")

        #Email confirmation
        current_site = get_current_site(request)
        email_subject = "Confirm your email - P24 Agenda"
        message = render_to_string("logs/email_confirmation.html", {
            "name": myuser.first_name, 
            "domain": current_site.domain, 
            "uid": urlsafe_base64_encode(force_bytes(medecin.user.pk)),
            "token": generate_token.make_token(medecin)
            })
        
        email = EmailMessage(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [medecin.user.email],
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

    patients = Patient.objects.filter(admin = Medecin.objects.get(user = request.user) )

    #Ici, on récupère les informations pour ajouter un patient
    if request.method == "POST":

        form1 = CustomUserForm(request.POST)
        form2 = PatientForm(request.POST)
    
        if form1.is_valid() and form2.is_valid():

            myuser_p = form1.save()
            mdp = myuser_p.last_name + "_" + myuser_p.first_name + "_"
            myuser_p.set_password( mdp )
            myuser_p.save()

            mypatient = form2.save(commit=False)
            mypatient.user = myuser_p
            mypatient.admin = Medecin.objects.get(user=request.user)
            mypatient.save()

            messages.success(request, "Informations récupérées avec succès !")

            #Envoyez un mail au patient pour activer et changer son MDP
            current_site = get_current_site(request)
            email_subject = "Your doctor" + request.user.last_name + "a activé votre compte - P24 Agenda."
            message = render_to_string("logs/email_confirmation.html", {
                "name": mypatient.user.first_name, 
                "domain": current_site.domain, 
                "uid": urlsafe_base64_encode(force_bytes(mypatient.user.pk)),
                "token": generate_token.make_token(mypatient)
                })
            
            email = EmailMessage(
                email_subject,
                message,
                settings.EMAIL_HOST_USER,
                [mypatient.user.email],
            )

            email.fail_silently = True
            email.send()

            return render(request, 'moncompte/compte.html', {'patients': patients, 'form1': form1, 'form2': form2, 'popupopen': False})
        
        else:
            
            messages.error(request, "Renseignement non valides !")
            print(form1.errors)
            print(form2.errors)
            return render(request, 'moncompte/compte.html', {'patients': patients, 'form1': form1, 'form2': form2, 'popupopen': True})

    else:
        form1 = CustomUserForm
        form2 = PatientForm

    return render(request, 'moncompte/compte.html', {'patients': patients, 'form1': form1, 'form2': form2, 'popupopen': False})

def agenda(request):
    
    return render(request, "accueil/weekly.html")

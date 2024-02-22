from datetime import timedelta, timezone, datetime, time
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from agenda.models import Medecin, CustomUser, Patient, Slot
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token
from merchex import settings
from django.contrib.auth import get_user_model
import json
from django.http import JsonResponse
from agenda.utils.slots import *
from .forms import PatientForm, CustomUserForm, MedecinForm, CustomUserFormMedecin


User = get_user_model()

# Create your views here.

def home(request):
    return render(request, "logs/index.html")

def signup(request):

    if request.method == "POST":

        form1 = CustomUserFormMedecin(request.POST)
        form2 = MedecinForm(request.POST)
        liste = json.loads( request.POST["ma_liste"] )

        if form1.is_valid() and form2.is_valid():

            myuser = form1.save()
            myuser.set_password(myuser.password)
            myuser.save()

            medecin = form2.save(commit = False)
            medecin.user = myuser
            medecin.save()

            populate_slots(liste, medecin)

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

        else:
            messages.error(request, 'Form incorrecte')
            print(form1.errors)
            print(form2.errors)
            return render(request, "logs/signup.html", {'form1': form1, 'form2': form2 })    
    
    else:
        form1 = CustomUserFormMedecin
        form2 = MedecinForm
        

    return render(request, "logs/signup.html", {'form1': form1, 'form2': form2 })

def signin(request):

    if request.method == "POST":

        username = request.POST['nom']
        mdp = request.POST['motdepasse']

        user = authenticate(username = username, password = mdp)

        if user is not None:
            login(request, user)
            prenom = user.first_name
            return redirect('agenda')
        
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

    #now = datetime.date.today()

    if request.method == 'POST':

        action = request.POST.get('action')
        if action == 'avancer':
            print("ON AVANCE")

            #On reçoit la date actuelle
            date_text = request.POST.get('date')

            print("DADADADA", date_text)
            now = datetime.datetime.strptime(date_text, '%Y-%m-%d')

        elif action == 'reculer':
            print("ON RECULE")

            #On reçoit la date actuelle
            date_text = request.POST.get('date')

            print("DADADADA", date_text)
            now = datetime.datetime.strptime(date_text, '%Y-%m-%d')

        slot = request.POST.get('slot')
        if slot is not None and slot.startswith('slot'):

            print("UNLOCK: ", slot)
            date_text = request.POST.get('date')
            print("DATE SLOT: ",date_text)
            now = datetime.datetime.strptime(date_text, '%Y-%m-%d')

            #Date du slot
            jour = request.POST.get('jour')
            print("jour: ", jour)
            jour_int = int(jour)
            date_slot = now + datetime.timedelta(days = jour_int)

            #Heure du slot
            slot = slot.split("_")
            heure = int(slot[2]) + 6
            heure_final = time(heure)

            #Médecin du slot
            medecin_connecte = Medecin.objects.get(user=request.user)

            #On recherche le slot correspondant
            try:

                slot_modif = Slot.objects.get(
                medecin=medecin_connecte,
                date=date_slot,
                heure_debut = heure_final
                )

                slot_modif.bloque = False
                slot_modif.save()

                print("Slot modified, it is now unlocked !")

                messages.success(request, 'Slot modified, it is now unlocked !')

            except Slot.DoesNotExist:
                messages.error(request, 'The slot does not exist, nothing changed')

            except Slot.MultipleObjectsReturned:
                messages.error(request, 'Multiple slots were found, nothing changed')





    else:
        #Sinon, on charge la date de cette semaine
        now = datetime.date.today()

    #On cherche les slots de cette semaine
    medecin_connecte = Medecin.objects.get(user=request.user)  
    jour_semaine = now.weekday()
    date = now - datetime.timedelta(days = jour_semaine)
    # print("DATE: " ,date )

    slots = []

    for i in range(6):

        date2 = date + datetime.timedelta(days = i)

        slots_du_medecin = Slot.objects.filter(
            medecin=medecin_connecte,
            date=date2
        )

        slots.append(slots_du_medecin)

        # print(len( slots ), "------------", slots[i], "----------", date2)

    #On envoie la date qu'il faut --> now
    return render(request, "accueil/weekly.html", {'slots': slots, 'date': now})

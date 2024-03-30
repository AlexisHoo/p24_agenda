from datetime import datetime, time, timedelta
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from agenda.models import Medecin, CustomUser, Patient, Slot
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from . tokens import generate_token
from django.contrib.auth import get_user_model
import json
from django.http import JsonResponse
from agenda.utils.slots import *
from agenda.utils.parser import *
from .forms import PatientForm, CustomUserForm, MedecinForm, CustomUserFormMedecin

#Email
from agenda.utils.email import *


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
            send_email(request, myuser, medecin)
        
            return redirect('signin')

        else:

            messages.error(request, 'Form incorrecte ')
                          
            if form1.errors:

                messages.error(request, form1.errors)
                print(form1.errors)

            elif form2.errors:
                messages.error(request, form2.errors)
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
            myuser_p.is_patient = True
            myuser_p.save()

            mypatient = form2.save(commit=False)
            mypatient.user = myuser_p
            mypatient.admin = Medecin.objects.get(user=request.user)
            mypatient.save()

            messages.success(request, "Informations récupérées avec succès !")

            #Envoyez un mail au patient pour activer et changer son MDP
            send_email_patient(request, mypatient)

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
    medecin_connecte = Medecin.objects.get(user=request.user)

    if request.method == 'POST':

        #Date
        now = datetime.datetime.strptime(request.POST.get('date'), '%Y-%m-%d').date()
        slot = request.POST.get('slot')
        
        if slot is not None and slot.startswith('slot'):

            print("SLOT: ", slot)
            #Parsing heure et date du jour cliqué
            heure = parser_heure(slot)
            slot = slot.split("_")
            jours = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']

            jour = jours.index(slot[3])
            date = now + datetime.timedelta(days = jour)
            
            if "unlock" in slot or "rdv" in slot:
                
                envoi_justification = False
                print("SUPPRESION RDV")
                if 'rdv' in slot:
                    envoi_justification = True

                supprimer_slot(heure, request, date, medecin_connecte, envoi_justification)
                return redirect(request.path)
                
            elif "lock" in slot:

                print("LOCK RDV")
                heures, minutes, heure_debut = parser_heure_debut(request, date, heure)

                #SECURITE A FAIRE, pour voir s'il n'y a pas un slot qui est sur cette plage horaire
                free = is_free(heures, minutes, date, heure_debut, medecin_connecte)

                if free:
                    slot_bloque = Slot.objects.create( medecin = Medecin.objects.get( user = request.user ), date = date, heure_debut = heure_debut, duree = datetime.timedelta(hours = heures, minutes= minutes), bloque = True) #datetime.timedelta(hours = 1)
                    slot_bloque.save()
                    print("     Slot bloqué créée ! Date: ", slot_bloque.date, '  heure: ', slot_bloque.heure_debut, "  duree: ", slot_bloque.duree)
                    messages.success(request, 'Slot modified, it is now locked !')
                else:
                    messages.error(request, "Le rdv que vous cherchez à bloquer n'est pas sur une plage horaire libre !")
                    print("     Slot pas disponible")

                return redirect(request.path)

            elif "add" in slot:

                print("AJOUT D'UN RDV")
                heures_duree, minutes_duree, heure_debut = parser_heure_debut(request, date, heure)

                #SECURITE A FAIRE, pour voir s'il n'y a pas un slot qui est sur cette plage horaire
                free = is_free(heures_duree, minutes_duree, date, heure_debut, medecin_connecte)

                if free:
                    add_slot(request, date, heure_debut, heures_duree, minutes_duree, medecin_connecte)
                else:
                    messages.error(request, "Le rdv que vous cherchez à réserver n'est pas sur une plage horaire libre !")
                    print("     Slot pas disponible")

                return redirect(request.path)

    else:
        #Sinon, on charge la date de cette semaine
        now = datetime.date.today()

    #Début de semaine
    jour_semaine = now.weekday()
    date = now - datetime.timedelta(days = jour_semaine)
    print("AFTER ALL: ", now)

    #On cherche les rdvs des jours de la semaine de la date correspondante
    print("FILL DAY")
    slots = []
    for i in range(6):

        date2 = date + datetime.timedelta(days = i)

        slots_du_medecin = Slot.objects.filter(
            medecin=medecin_connecte,
            date=date2
        )

        #On rempli le reste du jour avec des espaces disponibles
        print("JOUR ", i)
        slots_du_jour = [slot for slot in slots_du_medecin]
        full_day = fill_day(slots_du_jour, date2, medecin_connecte)

        slots.append(full_day)

    #On envoie la date qu'il faut --> now
    rdv = {'lundi':slots[0], 'mardi':slots[1],'mercredi':slots[2],'jeudi':slots[3],'vendredi':slots[4],'samedi':slots[5]}
    return render(request, "accueil/weekly.html", {'slots': slots, 'date': now, 'rdv' : rdv})

def add_rdv(request):

    if request.method == 'GET' and 'query' in request.GET:

        # print("requete get")
        query = request.GET.get('query')
        patients_users = CustomUser.objects.filter(last_name__icontains=query, is_patient = True) | CustomUser.objects.filter(first_name__icontains=query, is_patient = True)
        medecin_connecte = request.user.medecin
        patients = Patient.objects.filter(user__in=patients_users, admin=medecin_connecte)

        data = [{'nom': patient.user.last_name, 'prenom': patient.user.first_name} for patient in patients]

        # print("DATA: ", data)
        return JsonResponse(data, safe=False)
        
    else:
        if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            # Si la demande est une requête AJAX, renvoyer uniquement les données JSON
            patients = CustomUser.objects.filter(is_patient=True)
            data = [{'nom': patient.nom, 'prenom': patient.prenom} for patient in patients]
            return JsonResponse(data, safe=False)
        else:
            return render(request, "accueil/add_rdv.html")
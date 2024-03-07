from datetime import datetime, time
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

        action = request.POST.get('action')
        if action == 'avancer':

            #On reçoit la date actuelle
            date_text = request.POST.get('date')
            now = datetime.datetime.strptime(date_text, '%Y-%m-%d')

            print("AVANCER: ", now)

        elif action == 'reculer':

            #On reçoit la date actuelle
            date_text = request.POST.get('date')
            now = datetime.datetime.strptime(date_text, '%Y-%m-%d')
            print("RECULER: ", now)

        slot = request.POST.get('slot')
        if slot is not None and slot.startswith('slot'):

            print("SLOT: ", slot)

            if "unlock" in slot:

                #Médecin du slot
                # medecin_connecte = Medecin.objects.get(user=request.user)

                #Actualise la date
                now = datetime.datetime.strptime(request.POST.get('date'), '%Y-%m-%d')

                #On modifie le slot
                modifier_slot(False, slot, request, now, request.POST.get('date'), request.POST.get('jour'), medecin_connecte)
                
            elif "lock" in slot:

                #Médecin du slot
                # medecin_connecte = Medecin.objects.get(user=request.user)

                #Actualise la date
                now = datetime.datetime.strptime(request.POST.get('date'), '%Y-%m-%d')

                #On modifie le slot
                modifier_slot(True, slot, request, now, request.POST.get('date'), request.POST.get('jour'), medecin_connecte)

            elif "add" in slot:
                
                #On récupère l'heure et la date du slot
                slot = slot.split("_")
                heure = int(slot[2]) + 6
                now = datetime.datetime.strptime(request.POST.get('date'), '%Y-%m-%d')
                jour = int( request.POST.get('jour') )
                date = now + datetime.timedelta(days = jour)


                #On affiche la page ajout d'un rdv
                return render(request, "accueil/add_rdv.html", {'heure': heure, 'date': date})
            
            elif "rdv" in slot:

                #On récupère l'heure et la date du slot et le médecin
                slot = slot.split("_")
                heure = int(slot[2]) + 6
                now = datetime.datetime.strptime(request.POST.get('date'), '%Y-%m-%d')
                jour = int( request.POST.get('jour') )
                date = now + datetime.timedelta(days = jour)
                medecin_connecte = Medecin.objects.get(user=request.user)

                #On modifie le slot pour enlever le patient
                try:

                    rdv = Slot.objects.get(
                        date = date,
                        heure_debut = time(int(heure)),
                        medecin = medecin_connecte 
                    )

                    rdv.patient = None
                    rdv.note = "Aucunes notes"
                    rdv.save()
                    print("Slot supprimé ! Date: ", date, "  heure: ", heure)
                    messages.success(request, "Slot supprimé avec succès !")

                except:
                    print("Le slot n'existe pas ou plusieurs rdv ont été toruvé !")
                    messages.error(request, "Le slot n'existe pas ou plusieurs rdv ont été toruvé !")


    else:
        #Sinon, on charge la date de cette semaine
        now = datetime.date.today()

    #On cherche les slots de cette semaine
    # medecin_connecte = Medecin.objects.get(user=request.user)  
    jour_semaine = now.weekday()
    date = now - datetime.timedelta(days = jour_semaine)
    print("AFTER ALL: ", now)
    print("WEEKDAYS: ", jour_semaine)

    #On cherche les rdvs des jours de la semaine de la date correspondante
    slots = []
    for i in range(6):

        date2 = date + datetime.timedelta(days = i)

        slots_du_medecin = Slot.objects.filter(
            medecin=medecin_connecte,
            date=date2
        )

        slots.append(slots_du_medecin)

    #On envoie la date qu'il faut --> now
    return render(request, "accueil/weekly.html", {'slots': slots, 'date': now})

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
    
    elif request.method == 'POST':

        #Vérifier si le patient existe
        patient = request.POST.get("search").split(" ")
        nom = patient[0]
        prenom = patient[1]

        #Notes
        notes = request.POST.get("notes")

        #Heure et date 
        heure = request.POST.get("heure")
        date = request.POST.get("date")
        date = date.replace(', midnight', '').strip()
        date = datetime.datetime.strptime(date, '%b. %d, %Y').date()

        medecin = Medecin.objects.get( user = request.user )

        try:
            
            patient_rdv = CustomUser.objects.get(
                first_name = prenom,
                last_name = nom,
                is_patient = True
            )

            patient = Patient.objects.get(
                user = patient_rdv
            )

            #Vérifier si le docteur correspond
            if patient.admin == medecin:

                #Voir si le slot existe
                existe = Slot.objects.filter(
                    date = date, 
                    heure_debut = time(int(heure)),
                    medecin = medecin
                )

                if existe.exists():
                    #On modifie le slot existant
                    modif = existe.first()
                    modif.patient = patient
                    modif.bloque = False
                    print("Slot créée ! Date: ", date, '  heure: ', heure, "  patient: ", modif.patient)
                    modif.note = notes
                    modif.save()

                else:
                    #Sinon on crée le slot 
                    slot = Slot.objects.create( medecin = medecin, patient = patient, date = date, heure_debut = time(int(heure)), duree = datetime.timedelta(hours = 1), bloque = False, note = notes)
                    slot.save()
                    print("Slot créée ! Date: ", date, '  heure: ', heure, "  patient: ", slot.patient)

        except:
            messages.error(request, "Erreur, le patient n'existe pas ")

        return redirect('agenda')
    
        
    else:
        if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            # Si la demande est une requête AJAX, renvoyer uniquement les données JSON
            patients = CustomUser.objects.filter(is_patient=True)
            data = [{'nom': patient.nom, 'prenom': patient.prenom} for patient in patients]
            return JsonResponse(data, safe=False)
        else:
            return render(request, "accueil/add_rdv.html")
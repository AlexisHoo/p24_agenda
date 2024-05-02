from datetime import datetime, time, timedelta, timezone
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from agenda.models import Medecin, CustomUser, Patient, Slot, TypeRDV, Invitation
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from . tokens import generate_token
from django.contrib.auth import get_user_model
import json
from django.http import JsonResponse
from agenda.utils.slots import *
from agenda.utils.parser import *
from .forms import PatientForm, CustomUserForm, MedecinForm, CustomUserFormMedecin, MedecinFormBis, TypeRDVForm, InvitationForm
from bs4 import BeautifulSoup

#MDP
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

#Email
from agenda.utils.email import *


User = get_user_model()

# Create your views here.

def home(request):

    form1 = CustomUserFormMedecin
    form2 = MedecinForm

    return render(request, "logs/signin.html", {'form1': form1, 'form2': form2 })


def signin(request):

    if request.method == "POST":

        sign = request.POST['sign']
        print("SIGN: ", sign)

        if sign == "Se connecter":

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
        
        elif sign == "Créer un compte":

            form1 = CustomUserFormMedecin(request.POST)
            form2 = MedecinForm(request.POST)
            # liste = json.loads( request.POST["ma_liste"] )

            if form1.is_valid() and form2.is_valid():

                myuser = form1.save()
                myuser.set_password(myuser.password)
                myuser.save()

                medecin = form2.save(commit = False)
                medecin.user = myuser
                medecin.save()

                #Créer un type de RDV par défaut
                type_rdv = TypeRDV.objects.create(duree=timedelta(minutes=45), nom="HEY", medecin=medecin)
                type_rdv.save()

                #Create an invitation
                invit = Invitation.objects.create(medecin = medecin, nbr_RDV = 5, duree_RDV=timedelta(minutes=45), nbr_semaine = 5, modif_RDV = 3 )
                invit.save()

                # populate_slots(liste, medecin)
                messages.success(request, "Utilisateur enregistré. Nous vous avons envoyé un email de confirmation. Veuillez activer votre compte !")

                #Email confirmation
                send_email(request, myuser, medecin)

                return render(request, "logs/signin.html", {'form1': form1, 'form2': form2, 'version':False })

            else:
                            
                if form1.errors:

                    messages.error(request, form1.errors)
                    print(form1.errors)

                    # error_messages_html = ''.join(form1.errors.values())
                    error_messages_html = str(form1.errors)
                    soup = BeautifulSoup(error_messages_html, 'html.parser')

                    error_messages = [li.get_text() for li in soup.find_all('li')]
                    print("HEYYY: ", error_messages)

                elif form2.errors:
                    messages.error(request, form2.errors)
                    print(form2.errors)

                return render(request, "logs/signin.html", {'form1': form1, 'form2': form2, 'version':True })
    
    else:
        form1 = CustomUserFormMedecin
        form2 = MedecinForm
        version = False


    return render(request, "logs/signin.html", {'form1': form1, 'form2': form2, 'version':version })

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
    
def setup(request):

    medecin = Medecin.objects.get(user=request.user)
    print("SETUP")

    if request.method == 'POST':
        print("     POST")
        modif = request.POST.get('modif')
       
        if modif == 'modif':

            print("     CHANGE INFOS")
            form1 = MedecinFormBis(request.POST)

            if form1.is_valid():

                #On change les infos
                medecin.tel_medecin = form1.cleaned_data['tel_medecin']
                medecin.address_of_office = form1.cleaned_data['address_of_office']

                print("     TEL: ", form1.cleaned_data['tel_medecin'])
                print("     ADRESSE: ", form1.cleaned_data['address_of_office'])
            
                medecin.save()

                messages.success(request, "Vos informations ont été mises à jour !")

                form1 = MedecinFormBis(initial={'tel_medecin': medecin.tel_medecin, 'address_of_office': medecin.address_of_office})
                return redirect(request.path)

            else:
                messages.error(request, form1.errors)
                return render(request, 'setup/setup.html', {'medecin':medecin, 'form1': form1})
            
        elif modif == 'mdp':

            print("     MDP")

            actual_mdp = request.POST.get('actual_mdp')
            new_mdp = request.POST.get('new_mdp')
            confirm_mdp = request.POST.get('confirm_mdp')

            print("     ACTUAL: ", actual_mdp)
            print("     NEW: ", new_mdp)
            print("     CONFIRM: ", confirm_mdp)

            #Vérifier que c'est le bon mdp
            if check_password(actual_mdp, medecin.user.password):

                print("     ACTUAL CORRECT")
                if new_mdp == confirm_mdp:

                    print("     SAME")
                    medecin.user.set_password(new_mdp)
                    update_session_auth_hash(request, medecin.user)
                    medecin.user.save()

                    print(type(medecin.user))  # Vérifiez le type de l'objet user
                    print(medecin.user.id)

                else:
                    messages.error(request, "Les nouveaux mots de passe doivent être identiques!")
                
            else:
                messages.error(request, "Le mot de passe ne correspond pas!")
            
            return redirect(request.path)
        
        elif 'delete' in modif:
            print("     DELETE RDV")
            id = modif.split("_")[1]

            rdv = TypeRDV.objects.get(
                id = id
            )
            rdv.delete()

            return redirect(request.path)
        
        elif modif == 'create-rdv':

            print("     CRER TYPERDV")
            form2 = TypeRDVForm(request.POST)

            if form2.is_valid():

                print("     CORRECT")
                new_RDV = form2.save()
                print("     RDV: ", new_RDV)
                new_RDV.medecin = medecin
                new_RDV.save()
                print("     HEY")

            else:
                messages.error(request, form2.errors)
            
            return redirect(request.path)
        
        elif modif == 'invit':

            print("     INVIT")
            form3 = InvitationForm(request.POST)

            if form3.is_valid():

                print("     CORRECT")
                # new_invit = form3.save(commit=False)
                print("     TEMPS: ", str(form3.cleaned_data['duree_RDV'])[2:])
                str_date = str(form3.cleaned_data['duree_RDV'])[2:]

                invit = Invitation.objects.get(medecin = medecin)
                hours, minutes = map(int, str_date.split(':'))

                # Création d'un objet timedelta avec les minutes
                duration = timedelta(hours=hours, minutes=minutes)

                invit.nbr_RDV = form3.cleaned_data['nbr_RDV']
                invit.duree_RDV = duration
                invit.nbr_semaine = form3.cleaned_data['nbr_semaine']
                invit.modif_RDV = form3.cleaned_data['modif_RDV']

                invit.save()

                messages.success(request, "Votre invitation a été mise à jour !")
            
            else:
                messages.error(request, form3.errors)

            return redirect(request.path)

    else:
        invit = Invitation.objects.get(medecin = medecin)
        form1 = MedecinFormBis(initial={'tel_medecin': medecin.tel_medecin, 'address_of_office': medecin.address_of_office})
        form2 = TypeRDVForm()
        form3 = InvitationForm(initial={'nbr_RDV': invit.nbr_RDV, 'duree_RDV': invit.duree_RDV, 'nbr_semaine': invit.nbr_semaine, 'modif_RDV': invit.modif_RDV})


    #Avoir les différents types de RDV
    typesRDV = TypeRDV.objects.filter(
        medecin = medecin
    )
    medecin = Medecin.objects.get(user = request.user)

    return render(request, 'setup/setup.html', {'medecin':medecin, 'form1': form1, 'form2': form2,'form3': form3,  'typesRDV': typesRDV})

def patients(request):

    patients = Patient.objects.filter(admin = Medecin.objects.get(user = request.user) )

    # for i in patients:
    #     print(" NBRRDV: ", i.invitation.nbr_RDV, i)


    print("PATIENTS")

    #Ici, on récupère les informations pour ajouter un patient
    if request.method == "POST":

        print("     POST")
        form1 = CustomUserForm(request.POST)
        form2 = PatientForm(request.POST, admin=Medecin.objects.get(user=request.user))
        form3 = InvitationForm(request.POST)
        compte = request.POST.get('compte')
        print("     COMPTE", compte)
        if compte == 'ajout':

            print("     CREER PATIENT")

            if form1.is_valid() and form2.is_valid():

                myuser_p = form1.save()

                #On crée le user et la patient associé
                mdp = myuser_p.last_name + "_" + myuser_p.first_name + "_"
                myuser_p.set_password( mdp )
                myuser_p.is_patient = True
                myuser_p.save()

                mypatient = form2.save(commit=False)
                mypatient.user = myuser_p
                mypatient.admin = Medecin.objects.get(user=request.user)
                mypatient.save()


                #Create an invitation
                invit = Invitation.objects.create(patient = mypatient, nbr_RDV = 5, duree_RDV=timedelta(minutes=45), nbr_semaine = 5, modif_RDV = 3 )
                invit.save()

                messages.success(request, "Informations récupérées avec succès !")

                #Envoyez un mail au patient pour activer et changer son MDP
                send_email_patient(request, mypatient)
            
            else:
        
                messages.error(request, form1.errors)
                messages.error(request, form2.errors)
                print(form1.errors)
                print(form2.errors)
                return render(request, 'moncompte/compte.html', {'patients': patients, 'form1': form1, 'form2': form2, 'form3': form3, 'popupopen': True})


        elif compte == 'modif':
            #On modifie le patient
            print("     MODIFIER PATIENT")

            if form2.is_valid():

                print("     VALID")
                username_test = request.POST.get('username_modif')
                email_test = request.POST.get('email_modif')

                print("     INFOS: ", username_test, email_test)

                #Voir si le user existe déjà
                user = CustomUser.objects.filter(
                    username = username_test,
                    email = email_test
                ).first()

                print("     USER: ", user)

                if user:
                
                    #trouver le patient associé à ce user
                    patient = Patient.objects.get(
                        user = user
                    )

                    print("     PATIENT ASSOCIE: ", patient)

                    new_infos = form2.save(commit=False)
                    patient.tel_patient = new_infos.tel_patient
                    patient.adresse_patient = new_infos.adresse_patient
                    patient.numero_secu = new_infos.numero_secu
                    patient.couleur_patient = new_infos.couleur_patient
                    patient.sexe = new_infos.sexe
                    patient.date_naissance = new_infos.date_naissance
                    patient.type_rdv = new_infos.type_rdv
                    patient.save()

            else:
                messages.error(request, "Renseignement non valides !")
                print(form1.errors)
                print(form2.errors)
                return render(request, 'moncompte/compte.html', {'patients': patients, 'form1': form1, 'form2': form2, 'form3': form3, 'popupopen': True})

        elif compte == 'invit':

            print("     INVIT PATIENT")

            if form3.is_valid():

                print("     CORRECT")

                id_patient = request.POST.get('id_patient')

                print("     ID PATIENT: ", id_patient)
                patient = Patient.objects.get(
                    pk = id_patient
                    )

                print("     PATIENT: ", patient)

                invit = patient.invitation
                invit.nbr_RDV = form3.cleaned_data['nbr_RDV']
                invit.duree_RDV = form3.cleaned_data['duree_RDV']
                invit.nbr_semaine = form3.cleaned_data['nbr_semaine']
                invit.modif_RDV = form3.cleaned_data['modif_RDV']
                invit.date_limite = datetime.date.today()
                invit.date_limite = invit.date_limite + timedelta(weeks=invit.nbr_semaine)

                print("     DATE LIMITE: ", invit.date_limite)

                invit.save()
                print("     YEAH")

                messages.success(request, "Votre invitation a été enregistré !")
            
            else:
                messages.error(request, form3.errors)

            return redirect(request.path)

        return render(request, 'moncompte/compte.html', {'patients': patients, 'form1': form1, 'form2': form2, 'form3': form3, 'popupopen': False})
  
    else:
        print("     GET")
        medecin = Medecin.objects.get(user=request.user)
        form1 = CustomUserForm
        form2 = PatientForm(admin=medecin)
        invit = Invitation.objects.get(medecin = medecin)
        form3 = InvitationForm(initial={'nbr_RDV': invit.nbr_RDV, 'duree_RDV': invit.duree_RDV, 'nbr_semaine': invit.nbr_semaine, 'modif_RDV': invit.modif_RDV})


    return render(request, 'moncompte/compte.html', {'patients': patients, 'form1': form1, 'form2': form2, 'form3': form3, 'popupopen': False})

def agenda(request):

    #now = datetime.date.today()
    medecin_connecte = Medecin.objects.get(user=request.user)

    if request.method == 'POST':

        #Date
        
        request.session['date'] = request.POST.get('date')
        now = datetime.datetime.strptime(request.POST.get('date'), '%Y-%m-%d').date()
        slot = request.POST.get('slot')
        print("SLOT: ", slot)
        
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
                messages.success(request, "La plage horaire a été supprimée !")
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
                    messages.success(request, 'La plage horaire est maintenant bloquée !')
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
            
            elif "notes" in slot:

                print("MODIFIER NOTES")
                #nouvelles notes
                notes = request.POST.get('note')
                print("     NOTES: ", notes)
                print("     DATE: ", date, " heure début: ", heure)

                #Aller chercher le slot et le modifier avec a nouvelle notes
                try:

                    rdv = Slot.objects.get(
                        date = date,
                        heure_debut = heure,
                        medecin = medecin_connecte
                    )

                    rdv.note = notes
                    rdv.save()
                    print("     RDV MODIFIE")
                    messages.success(request, "Notes enregistrées !")
                
                except:
                    messages.error(request, "RDV non trouvé, veuillez réessayer !")

                return redirect(request.path)


    else:
        #Sinon, on charge la date de cette semaine
        print("REQUETE GET")
        defaut = str(datetime.date.today())
        now = datetime.datetime.strptime(request.session.get('date', defaut), '%Y-%m-%d').date()

        print("     NOW:", now)

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
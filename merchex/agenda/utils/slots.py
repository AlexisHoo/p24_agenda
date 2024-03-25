from agenda.models import Medecin, CustomUser, Patient, Slot
import datetime
from datetime import time
from django.contrib import messages
from agenda.utils.parser import *


def populate_slots(liste, medecin):

    now = datetime.date.today()
    jour_semaine = now.weekday()
    date_slot = now - datetime.timedelta(days = jour_semaine)

    #On parcours la semaine
    for i in range( len(liste) ):

        #On mets à jour la date de la semaine
        date_slot2 = date_slot + datetime.timedelta(days = i)

        # On parcours de 7h à 20
        for j in range( len( liste[i] )):

            if liste[i][j] == True:

                print("date: ",date_slot2, " heure: ", (j + 7) )

                #Si le slot a été cliqué, on créée un slot
                slot = Slot.objects.create(
                    medecin = medecin,
                    date = date_slot2,
                    heure_debut = datetime.time(hour = j + 7), #+7 car de 7h à 20h
                    duree = datetime.timedelta(hours = 1),
                    bloque = True
                )
                slot.save()


def supprimer_slot(heure, request, date_slot, medecin):

    print("SUPPRESSION","\n     medecin: ", medecin, " heure: ", heure, " date: ", date_slot)
    #On recherche le slot correspondant si on veut le unlock (le supprimer)
    try:

        slot_modif = Slot.objects.get(
        medecin=medecin,
        date=date_slot,
        heure_debut = heure
        )
        slot_modif.delete()
        
        print('     Slot unlocked ! Date: ', date_slot , ' ', heure)   
        messages.success(request, 'Slot unlocked !')

    except Slot.DoesNotExist:
        print("     Slot does not exist !")
            

    except Slot.MultipleObjectsReturned:
        messages.error(request, 'Multiple slots were found, nothing changed')
        print("     Plusieurs slots trouvés !")
        slot_modif_mult = Slot.objects.filter(
        medecin=medecin,
        date=date_slot,
        heure_debut = heure
        )
        slot_modif_mult.delete()

def add_slot(request, date, heure_debut, heure_duree, minute_duree, medecin):

    #Vérifier si le patient existe
    patient = request.POST.get("search").split(" ")
    nom = patient[0]
    prenom = patient[1]

    #Notes
    notes = request.POST.get("notes")

    print("     Medecin: ", medecin, " -patient: ", nom, prenom, " -notes: ", notes)
    print("     date et heure: ", date, heure_debut, " -duree: ", heure_duree,":", minute_duree)

    try:
        print("     OK")
        patient_rdv = Patient.objects.filter(
            user__first_name = prenom,
            user__last_name = nom,
            # is_patient = True
            admin = medecin
        ).first()

        print("     OK")

        # print("On a trouvé le patient: ", patient_rdv)

        #Voir si le slot existe
        # existe = Slot.objects.filter(
        #     date = date, 
        #     heure_debut = heure_debut,
        #     medecin = medecin
        # )

        # if existe:
        #     #On modifie le slot existant
        #     # print("le slot existe, on le modifie")
        #     modif = existe.first()
        #     modif.patient = patient_rdv
        #     modif.bloque = False
        #     print("     Slot créée ! Date: ", date, '  heure: ', heure_debut, "  patient: ", modif.patient)
        #     modif.note = notes
        #     modif.save()

        # else:
        #Sinon on crée le slot 
        # print("Le slot n'existe pas, on le crée")

        slot = Slot.objects.create( medecin = medecin, patient = patient_rdv, date = date, heure_debut = heure_debut, duree = datetime.timedelta(hours = int( heure_duree ), minutes= int( minute_duree )), bloque = False, note = notes)
        print("     OK")
        slot.save()
        print("     OK")
        print("     Slot créée ! Date: ", date, '  heure: ', heure_debut," -duree: ",slot.duree, "  patient: ", slot.patient)

    except:
        messages.error(request, "Erreur, le patient n'existe pas ")


def fill_day(rdvs, date, medecin):

    index = 0
    heure = time(7,0)
    while heure != time(20,0):

        #S'il ya un slot à cette heure
        # print('Heure à tester: ', heure)
        slot_existe = any(rdv.heure_debut == heure for rdv in rdvs)
        # print("slot existe: ", slot_existe)

        if not slot_existe:
        #On test jusqu'à ce qu'il n'y ai pas de slot

            # print("Il n'existe pas de slot")
            duree = 0
            heure_debut = heure
            #while il n'y a pas de slot, on fait +15 min
            while not slot_existe:

                # Ajouter 15 minutes
                heures = heure.hour
                minutes = heure.minute

                # Ajouter 15 minutes
                nouvelles_minutes = (minutes + 15) % 60
                nouvelles_heures = heures + (minutes + 15) // 60
                heure = time(nouvelles_heures, nouvelles_minutes)
                # print("+15min: ", heure)

                slot_existe = any(rdv.heure_debut == heure for rdv in rdvs)
                # print("slot existe ? : ", slot_existe)

                #On additione la durée du slot de +15 min
                duree += 15

                #Tester si il est 21h
                if heure == time(20,0):
                    break;

            #Il y a un slot, on ajoute la durée du "vide"
            slot_ajout = Slot( medecin = medecin, date = date, heure_debut = heure_debut, duree = datetime.timedelta(minutes = duree), bloque = False)
            print("     Slot créée ! Date: ", slot_ajout.date, '  heure: ', slot_ajout.heure_debut, "  duree: ", slot_ajout.duree)
            rdvs.insert(index, slot_ajout)
            # print(rdvs)
            index += 1

        else:
            index += 1
            #On avance de la durée du slot trouvé
            duree = [rdv.duree for rdv in rdvs if rdv.heure_debut == heure]
            print("     Duree du slot trouve: ", duree[0].seconds // 3600,":", (duree[0].seconds % 3600) // 60)
            ajout = time(duree[0].seconds // 3600, (duree[0].seconds % 3600) // 60)

            heures = heure.hour
            minutes = heure.minute

            # Ajouter 15 minutes
            nouvelles_minutes = (minutes + ajout.minute) % 60
            nouvelles_heures = ajout.hour + heures + (minutes + ajout.minute) // 60

            heure = time(nouvelles_heures, nouvelles_minutes)

    return rdvs

def is_free(heures, minutes, date, heure_debut, medecin):

    libre = False

    #Heure de fin 
    print("SECURITE")
    heures_debut = heure_debut.hour
    minutes_debut = heure_debut.minute

    nouvelles_minutes = (minutes_debut + minutes) % 60
    nouvelles_heures = heures_debut + (minutes_debut + minutes) // 60
    nouvelles_heures = nouvelles_heures + heures
    heure_fin = time(nouvelles_heures, nouvelles_minutes)

    print("     Slot à tester: ", date, " -heure debut: ", heure_debut, " -heure fin: ", heure_fin)

    # try:

    #Pour chaque slot du jour, on test si l'heure de début/fin du slot à tester est entre l'heure de début/fin du slot du jour
    list_slot_jour = Slot.objects.filter(
        date = date,
        medecin = medecin
    )

    if len(list_slot_jour) == 0:
        print("     Slot LIBRE (aucun autre rdv ajd)")
        libre = True

    else:

        for slot in list_slot_jour:
            
            fin = slot.get_heure_fin()
            print("     Slot du jour: ", slot.heure_debut, fin)
            #Si heure debut est entre heure debut/fin du slot
            if is_between(heure_debut, slot.heure_debut, fin) == False:

                #Si heure fin est entre heure debut/fin du slot
                if is_between(heure_fin, slot.heure_debut, fin) == False:

                    #le slot est libre
                    # print("     SLOT LIBRE (pour l'instant)")
                    libre = True

                else:
                    print("     SLOT INCORRECT")
                    libre = False
                    break;
            
            else:
                print("     SLOT INCORRECT")
                libre = False
                break;
    
    # except:
    #     print("ERROR")
    #     libre = True

    return libre
        
def is_between(target_time, start_time, end_time):

    result = True
    # print("     IS BETWEEN")
    #Savoir si une heure est entre deux heures précisées
    target_seconds = time_to_seconds(target_time)
    start_seconds = time_to_seconds(start_time)
    end_seconds = time_to_seconds(end_time)

    if start_seconds < target_seconds:
        # print("     plus grand que le debut")

        if target_seconds < end_seconds:
            # print("     plus petit que la fin")
            result = True

        else:
            result = False
    
    else:
        result = False
    

    # print("     RESULT IS BETWEEN: ", result)
    return result

def time_to_seconds(t):
    return t.hour * 3600 + t.minute * 60 + t.second
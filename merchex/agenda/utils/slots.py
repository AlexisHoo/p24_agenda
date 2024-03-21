from agenda.models import Medecin, CustomUser, Patient, Slot
import datetime
from datetime import time
from django.contrib import messages


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
            
            # else:
                
            #     slot = Slot.objects.create(
            #         medecin = medecin,
            #         date = date_slot2,
            #         heure_debut = datetime.time(hour = j + 7), #+7 car de 7h à 20h
            #         duree = datetime.timedelta(hours = 1),
            #         bloque = False
            #     )


def modifier_slot(bloque, slot, request, now, date, jour, medecin):

    #Date du slot
    jour_int = int(jour)
    date_slot = now + datetime.timedelta(days = jour_int)

    #Heure du slot
    slot = slot.split("_")
    heure = slot[2]
    if "a.m." in heure:
        heure = heure.replace("a.m.", "AM")
    else:
        heure = heure.replace("p.m.", "PM")

    try:
        heure = datetime.datetime.strptime(heure, "%I:%M %p")
    except:
        # Si les minutes ne sont pas précisées, les considérer comme 00
        heure = datetime.datetime.strptime(heure, "%I %p")

    heure_final = heure.time()

    # print("medecin: ", medecin, " heure: ", heure_final, " date: ", date_slot)


    #On recherche le slot correspondant
    try:

        slot_modif = Slot.objects.get(
        medecin=medecin,
        date=date_slot,
        heure_debut = heure_final
        )

        slot_modif.bloque = bloque
        slot_modif.save()

        if bloque == True:
            print("Slot locked ! Date: ", date_slot , ' ', heure_final)   
            messages.success(request, 'Slot modified, it is now unlocked !')
        
        elif bloque == False:
            print('Slot unlocked ! Date: ', date_slot , ' ', heure_final)   
            messages.success(request, 'Slot unlocked !')

    except Slot.DoesNotExist:
        messages.error(request, 'The slot does not exist, nothing changed')

    except Slot.MultipleObjectsReturned:
        messages.error(request, 'Multiple slots were found, nothing changed')

def add_slot(request, heure, date):

    #Vérifier si le patient existe
    patient = request.POST.get("search").split(" ")
    nom = patient[0]
    prenom = patient[1]

    #Notes
    notes = request.POST.get("notes")

    medecin = Medecin.objects.get( user = request.user )

    try:
        patient_rdv = Patient.objects.filter(
            user__first_name = prenom,
            user__last_name = nom,
            # is_patient = True
            admin = medecin
        ).first()


        #Voir si le slot existe
        existe = Slot.objects.filter(
            date = date, 
            heure_debut = heure,
            medecin = medecin
        )

        if existe:
            #On modifie le slot existant
            modif = existe.first()
            modif.patient = patient_rdv
            modif.bloque = False
            print("Slot créée ! Date: ", date, '  heure: ', heure, "  patient: ", modif.patient)
            modif.note = notes
            modif.save()

        else:
            #Sinon on crée le slot 
            slot = Slot.objects.create( medecin = medecin, patient = patient_rdv, date = date, heure_debut = time(int(heure)), duree = datetime.timedelta(hours = 1), bloque = False, note = notes)
            slot.save()
            print("Slot créée ! Date: ", date, '  heure: ', heure, "  patient: ", slot.patient)

    except:
        messages.error(request, "Erreur, le patient n'existe pas ")
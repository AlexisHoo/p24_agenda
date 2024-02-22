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
            
            else:
                
                slot = Slot.objects.create(
                    medecin = medecin,
                    date = date_slot2,
                    heure_debut = datetime.time(hour = j + 7), #+7 car de 7h à 20h
                    duree = datetime.timedelta(hours = 1),
                    bloque = False
                )


def modifier_slot(bloque, slot, request, now, date, jour, medecin):

    date_text = date
    # print("DATE SLOT: ",date_text)
    

    #Date du slot
    jour = jour
    # print("jour: ", jour)
    jour_int = int(jour)
    date_slot = now + datetime.timedelta(days = jour_int)

    #Heure du slot
    slot = slot.split("_")
    heure = int(slot[2]) + 6
    heure_final = time(heure)
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
            # print("Slot modified, it is now locked !")   
            messages.success(request, 'Slot modified, it is now unlocked !')
        
        elif bloque == False:
            # print("Slot modified, it is now unlocked !")   
            messages.success(request, 'Slot modified, it is now unlocked !')

    except Slot.DoesNotExist:
        messages.error(request, 'The slot does not exist, nothing changed')

    except Slot.MultipleObjectsReturned:
        messages.error(request, 'Multiple slots were found, nothing changed')
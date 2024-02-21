from agenda.models import Medecin, CustomUser, Patient, Slot
import datetime


def populate_slots(liste, medecin):

    now = datetime.date.today()
    jour_semaine = now.weekday()
    date_slot = now - datetime.timedelta(days = jour_semaine)

    #On parcours la semaine
    for i in range( len(liste) ):

        #On mets à jour la date de la semaine
        date_slot = date_slot + datetime.timedelta(days = i)

        # On parcours de 7h à 20
        for j in range( len( liste[i] )):

            if liste[i][j] == True:

                print("date: ",date_slot, " heure: ", (j + 7) )

                #Si le slot a été cliqué, on créée un slot
                slot = Slot.objects.create(
                    medecin = medecin,
                    date = date_slot,
                    heure_debut = datetime.time(hour = j + 7), #+7 car de 7h à 20h
                    duree = datetime.timedelta(hours = 1),
                    bloque = True
                )
                slot.save()
            
            else:
                
                slot = Slot.objects.create(
                    medecin = medecin,
                    date = date_slot,
                    heure_debut = datetime.time(hour = j + 7), #+7 car de 7h à 20h
                    duree = datetime.timedelta(hours = 1),
                    bloque = False
                )



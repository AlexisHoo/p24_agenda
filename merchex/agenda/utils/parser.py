import datetime
from datetime import time


def parser_heure(slot):
    #On récupère l'heure du slot
    slot = slot.split("_")

    #Heure
    heure = slot[2]
    if "a.m." in heure:
        heure = heure.replace("a.m.", "AM")
    elif "p.m." in heure:
        heure = heure.replace("p.m.", "PM")
    else:
        #Noon
        heure = "12 PM"

    try:
        heure = datetime.datetime.strptime(heure, "%I:%M %p")
    except:
        heure = datetime.datetime.strptime(heure, "%I %p")
    
    return heure.time()

def parser_heure_debut(request, date, heure):
    duree = request.POST.get("duree")
    heure_debut = request.POST.get("heure")

    heures_duree = int( duree[0:2] )
    minutes_duree = int( duree[3:5] )

    heures_debut = int( heure_debut[0:2] )
    minutes_debut = int( heure_debut[3:5] )
    heure_debut = time(heures_debut, minutes_debut)

    print("     Infos RDV à ajouter: " , date, " ", heure)
    print("     -heure: ", heures_duree, ":", minutes_duree, " -heure debut: ", heure_debut)

    return heures_duree, minutes_duree, heure_debut
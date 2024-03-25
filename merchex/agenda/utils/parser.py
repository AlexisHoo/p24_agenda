import datetime


def parser_heure(slot):
    #On récupère l'heure du slot
    slot = slot.split("_")

    #Heure
    heure = slot[2]
    if "a.m." in heure:
        heure = heure.replace("a.m.", "AM")
    else:
        heure = heure.replace("p.m.", "PM")

    try:
        heure = datetime.datetime.strptime(heure, "%I:%M %p")
    except:
        heure = datetime.datetime.strptime(heure, "%I %p")
    
    return heure.time()
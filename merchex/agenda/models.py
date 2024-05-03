from datetime import datetime, time, timedelta, timezone
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_medecin = models.BooleanField(default=False)

    email = models.EmailField(blank=False, null=False)  # Rendre l'email unique
    first_name = models.CharField(max_length=30, blank=False, null=False)  # Champ obligatoire
    last_name = models.CharField(max_length=30, blank=False, null=False)
    #username
    #password
    #email
    #first_name
    #last_name
    #is_active

# Create your models here.
class Medecin(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)

    tel_medecin = models.CharField(max_length=15, blank=False, null=False, help_text="Format : +XX XXX XXX XXX")
    profession = models.CharField(max_length=25, blank=False, null=False)

    COLOR_CHOICES = [
        ('#0000FF', 'Bleu'),
        ('#FF0000', 'Rouge'),
        ('#FFFF00', 'Jaune'),
    ]
    couleur_medecin = models.CharField(max_length=20, default='Bleu', choices=COLOR_CHOICES)
    address_of_office = models.TextField(blank=True, null=True)
    #foreign key patients

class TypeRDV(models.Model):
    duree = models.DurationField(blank=False, default=timedelta(minutes=45))
    nom = models.CharField(max_length=25, blank=False, null=False, help_text="Type de RDV")

    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nom  # Renvoie le nom du type de RDV comme représentation de l'objet
    
    def id(self):
        return self.id



class Patient(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    admin = models.ForeignKey(Medecin, on_delete=models.CASCADE)
    type_rdv = models.ForeignKey(TypeRDV, on_delete=models.CASCADE, null=True)

    tel_patient = models.CharField(max_length=15, blank=False, null=False, help_text="Format : +XX XXX XXX XXX", default="+33 456 456 456")
    adresse_patient = models.TextField(blank=True, null=True)
    #foreignkey respo légaux
    numero_secu = models.CharField(max_length=16, blank=False, null=False, help_text="Format: XXXXXXXXXXXXX XX", default="1234567891234 56")
    COLOR_CHOICES = [
        ('#0000FF', 'Bleu'),
        ('#FF0000', 'Rouge'),
        ('#FFFF00', 'Jaune'),
    ]
    couleur_patient = models.CharField(max_length=7, default='#0000FF', choices=COLOR_CHOICES)
    SEX_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
        ('O', 'Autre'),
    ]
    sexe = models.CharField(max_length=1, choices=SEX_CHOICES)
    date_naissance = models.DateField(null=True, blank=True)

    def patient_id(self):
        return self.user.id
    
    def count_nbr_rdv(self):

        return self.slot_set.count()
    
    def next_rdv(self):

        today = datetime.now().date()

        #Prendre tous les rdv et regarder lequel est le plus proche 
        prochain_rdv = Slot.objects.filter(patient=self, date__gte=today).order_by('date')

        if len(prochain_rdv) != 0:
            print("     PROCHAIN: ", prochain_rdv)
            int_mois = int( str(prochain_rdv[0].date)[5:7] )
            int_jour = str(prochain_rdv[0].date)[8:10]
            mois = ['Janv.', 'Fév.','Mars', 'Avril', 'Mai', 'Juin', 'Juillet','Août', 'Sept.','Oct.','Nov.','Déc.']

            if int_jour.startswith('0'):
                int_jour = int_jour[1:2]

            string = int_jour +' ' + mois[int_mois - 1] + ' à ' + str(prochain_rdv[0].heure_debut)[0:5]

            return string

        else:
            return 'Pas de RDV réservé encore...'


class RDVPatient(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    type_rdv = models.ForeignKey(TypeRDV, on_delete=models.CASCADE)
  
class Slot(models.Model):

    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)#Si le slot est bloqué, il n'a pas de patient

    date = models.DateField(null=True, blank=True)
    heure_debut = models.TimeField(null=True, blank=True)
    duree = models.DurationField(null=True, blank=True)
    bloque = models.BooleanField(default=False) #Faux si un slot de RDV, Vrai si un slot bloqué par le médecin
    note = models.CharField(max_length=400, default="Aucunes notes")

    def get_vertical_position(self):

        if self.heure_debut:
            total_minutes = (self.heure_debut.hour - 7) * 35
            total_minutes = total_minutes + ( self.heure_debut.minute * 35 ) / 60
            # print("Heure debut: ", self.heure_debut.hour,":",self.heure_debut.minute, " -Top position: ", total_minutes)

            return total_minutes
        else:
            return 0
        
    def get_height(self):

        if self.duree:
            heures = ( self.duree.seconds // 3600)
            minutes = ( self.duree.seconds // 60 ) % 60 
            # print("Heure et minutes get: ", heures, minutes)

            hauteur = heures * 35 - 3
            hauteur = hauteur + (minutes * 35) / 60 #Produit en croix pour remettre sur 40 les minutes en plus
            # print("longueur: ", hauteur, "\n")
            return hauteur
        else:
            return 0
    
    def get_heure_fin(self):
        if self.heure_debut:
            
            heures = self.heure_debut.hour
            minutes = ( self.heure_debut.minute // 60 ) % 60

            minutes_ajout = ( self.duree.seconds // 60 ) % 60
            heures_ajout = ( self.duree.seconds // 3600)
            
            nouvelles_minutes = (minutes + minutes_ajout) % 60
            nouvelles_heures = heures + ( ( minutes + minutes_ajout ) // 60 ) + heures_ajout
            heure = time(nouvelles_heures, nouvelles_minutes)

            # final = str(nouvelles_heures) + ":" + str(nouvelles_minutes)

            return heure
        
    def get_heure_fin_str(self):
        if self.heure_debut:
            
            heures = self.heure_debut.hour
            minutes = ( self.heure_debut.minute // 60 ) % 60

            minutes_ajout = ( self.duree.seconds // 60 ) % 60
            heures_ajout = ( self.duree.seconds // 3600)
            
            nouvelles_minutes = (minutes + minutes_ajout) % 60
            nouvelles_heures = heures + ( ( minutes + minutes_ajout ) // 60 ) + heures_ajout
            # heure = time(nouvelles_heures, nouvelles_minutes)

            final = ''
            if nouvelles_minutes == 0:
                final = str(nouvelles_heures) + ":" + str(nouvelles_minutes) + "0"
            else:
                final = str(nouvelles_heures) + ":" + str(nouvelles_minutes)

            return final
        

        
        else:
            return 0
        
    def get_heure_str(self):
        if self.heure_debut:
            heures = self.heure_debut.hour
            minutes = ( self.heure_debut.minute // 60 ) % 60

            final = ''
            if minutes == 0:
                final = str(heures) + ":" + str(minutes) + "0"
            else:
                final = str(heures) + ":" + str(minutes)

            return final


class Invitation(models.Model):

    patient = models.OneToOneField(Patient, null=True, on_delete=models.CASCADE)
    medecin = models.OneToOneField(Medecin, null=True, on_delete=models.CASCADE)

    nbr_RDV = models.IntegerField(null=False, blank=True, default=5)
    # duree_RDV = models.DurationField(blank=False, default=timedelta(minutes=45))
    nbr_semaine = models.IntegerField(null=False, blank=True, default=5)
    modif_RDV = models.IntegerField(null=False, blank=True, default=5) #nbr de jours avant lesquels le patient peut modifier son RDV
    date_limite = models.DateField(null=True, blank=True)

    def is_active(self):

        today = datetime.now().date()

        if self.date_limite:

            if today < self.date_limite:
                print("     ACTIVE")
                return True
            else:
                print("     NON ACTIVE")
                return False
            
        else:
            print("     NON ACTIVE")
            return False



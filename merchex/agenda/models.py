from datetime import time
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

class Patient(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    admin = models.ForeignKey(Medecin, on_delete=models.CASCADE)

    tel_patient = models.CharField(max_length=15, blank=True, null=True, help_text="Format : +XX XXX XXX XXX")
    adresse_patient = models.TextField(blank=True, null=True)
    #foreignkey respo légaux
    numero_secu = models.CharField(max_length=16, blank=True, null=True, help_text="Format: XXXXXXXXXXXXX XX")
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

            return total_minutes  # Multipliez par 40 pour obtenir la position en pixels
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

        heures_debut = self.heure_debut.hour
        minutes_debut = ( self.heure_debut.second // 60 ) % 60
        heures_ajout = ( self.duree.seconds // 3600)
        minutes_ajout = ( self.duree.seconds // 60 ) % 60

        nouvelles_minutes = ( minutes_debut + minutes_ajout ) % 60
        nouvelles_heures = heures_debut + ( ( minutes_debut + minutes_ajout ) // 60 ) + heures_ajout

        return time(nouvelles_heures, nouvelles_minutes)


class Invitation(models.Model):

    nbr_RDV = models.IntegerField(null=True, blank=True)
    duree_RDV = models.DurationField(null=True, blank=True)
    nbr_semaine = models.IntegerField(null=True, blank=True)
    modif_RDV = models.IntegerField(null=True, blank=True) #nbr de jours avant lesquels le patient peut modifier son RDV
    date_limite = models.DateField(null=True, blank=True)
    lundi =  models.JSONField(default = { "lundi": [7,12,19], "mardi": [7,12,19], "mercredi": [7,12,19], "jeudi": [7,12,19], "vendredi": [7,12,19], "samedi": [7,12,19], "lundi": [7,12,19],})#dictionnaire pour les horaires bloqués de base.


    
    





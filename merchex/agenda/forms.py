# forms.py
import re
from django import forms
from .models import Patient, CustomUser

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['tel_patient', 'adresse_patient', 'numero_secu', 'couleur_patient', 'sexe', 'date_naissance']
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_numero_secu(self):
        numero_secu = self.cleaned_data.get('numero_secu')
        print("Méthode clean_nuùero_secu appelée")
        if numero_secu:
            if not re.match(r'^\d{13}\s\d{2}$', numero_secu):
                raise forms.ValidationError("Le format du numéro de sécurité social est incorrect. Utilisez le format : XXXXXXXXXXXXX XX")
        return numero_secu

    def clean_tel_patient(self):
        tel_patient = self.cleaned_data.get('tel_patient')
        if tel_patient:
            if not re.match(r'^\+\d{1,3}\s\d{1,3}\s\d{1,3}\s\d{1,3}$', tel_patient):
                raise forms.ValidationError("Le format du numéro de téléphone est incorrect. Utilisez le format : +XX XXX XXX XXX")
        return tel_patient
    
class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name','last_name']



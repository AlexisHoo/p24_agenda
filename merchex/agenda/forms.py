# forms.py

from django import forms
from .models import Patient, CustomUser

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['tel_patient', 'adresse_patient', 'numero_secu', 'couleur_patient', 'sexe', 'date_naissance']
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
        }

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name','last_name']
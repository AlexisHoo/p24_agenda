# forms.py
import re
from django import forms
from .models import Patient, CustomUser, Medecin, TypeRDV, Invitation

class PatientForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        admin = kwargs.pop('admin', None)  # Récupérer l'objet Medecin
        super(PatientForm, self).__init__(*args, **kwargs)
        if admin:
            # Filtrer les types de RDV associés au médecin
            self.fields['type_rdv'].queryset = TypeRDV.objects.filter(medecin=admin)
            print("     ADMIN: ", admin)
            print("     RDVS: ", TypeRDV.objects.filter(medecin=admin))

    class Meta:
        model = Patient
        fields = ['tel_patient', 'adresse_patient', 'numero_secu', 'couleur_patient', 'sexe', 'date_naissance', 'type_rdv']
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_numero_secu(self):
        numero_secu = self.cleaned_data.get('numero_secu')
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


class MedecinForm(forms.ModelForm):
    class Meta:
        model = Medecin
        fields = ['tel_medecin', 'profession', 'couleur_medecin', 'address_of_office']

    def clean_tel_medecin(self):
        tel_medecin = self.cleaned_data.get('tel_medecin')
        if tel_medecin:
            if not re.match(r'^\+\d{1,3}\s\d{1,3}\s\d{1,3}\s\d{1,3}$', tel_medecin):
                raise forms.ValidationError("Le format du numéro de téléphone est incorrect. Utilisez le format : +XX XXX XXX XXX")
        return tel_medecin

class MedecinFormBis(forms.ModelForm):
    class Meta:
        model = Medecin
        fields = ['tel_medecin','address_of_office']

    def clean_tel_medecin(self):
        tel_medecin = self.cleaned_data.get('tel_medecin')
        if tel_medecin:
            if not re.match(r'^\+\d{1,3}\s\d{1,3}\s\d{1,3}\s\d{1,3}$', tel_medecin):
                raise forms.ValidationError("Le format du numéro de téléphone est incorrect. Utilisez le format : +XX XXX XXX XXX")
        return tel_medecin
    
class CustomDurationWidget(forms.TextInput):
    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.input_type = 'time'
        self.attrs['step'] = 900
    
class TypeRDVForm(forms.ModelForm):
    class Meta:
        model = TypeRDV
        fields = ['nom','duree']

        widgets = {
            'duree': CustomDurationWidget(),
        }
    
    def clean_tel_medecin(self):
        nom = self.cleaned_data.get('nom')
        if nom:
            if not re.match(r'^.{1,25}$', nom):
                raise forms.ValidationError("Limite de caractères de 25 !")
        return nom

class CustomUserFormMedecin(forms.ModelForm):
    password2 = forms.CharField(label='Confirmation du mot de passe', widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name','last_name', 'password','password2']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password != password2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned_data
    
class CustomTimeInput(forms.TimeInput):
    input_type = 'time'

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('format', '%H:%M')
        super().__init__(*args, **kwargs)
    
class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ['nbr_RDV', 'duree_RDV', 'nbr_semaine', 'modif_RDV']# , 'date_limite'

        widgets = {
            'duree_RDV': CustomTimeInput(),
        }
        


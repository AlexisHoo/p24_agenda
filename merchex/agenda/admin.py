from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Medecin

class MedecinAdmin(UserAdmin):
    # Ajoutez des configurations personnalisées si nécessaire
    pass
admin.site.register(Medecin, MedecinAdmin)

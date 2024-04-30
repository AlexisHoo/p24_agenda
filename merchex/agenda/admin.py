from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(CustomUser)
admin.site.register(Medecin)
admin.site.register(Patient)
admin.site.register(Slot)
admin.site.register(Invitation)
admin.site.register(TypeRDV)

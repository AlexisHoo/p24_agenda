from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Medecin(AbstractUser):
    tel = models.CharField(max_length=15, blank=True, null=True)
    profession = models.CharField(max_length=255, blank=True, null=True)
    color = models.CharField(max_length=20, blank=True, null=True)
    #fixed_schedule = models.TextField(blank=True, null=True, default="")
    address_of_office = models.TextField(blank=True, null=True)



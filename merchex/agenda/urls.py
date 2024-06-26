from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('patients', views.patients, name="patients"),
    path('agenda', views.agenda, name="agenda"),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
    path('add_rdv/', views.add_rdv, name="add_rdv"),
    path('setup', views.setup, name="setup"),
]
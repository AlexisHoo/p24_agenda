from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('compte', views.compte, name="compte"),
    path('agenda', views.agenda, name="agenda"),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
    path('popup_slot', views.popup_slot, name="popup_slot"),
]
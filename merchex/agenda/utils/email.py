from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from ..tokens import generate_token
from merchex import settings

def send_email(request, myuser, medecin):
    #Email confirmation
    current_site = get_current_site(request)
    email_subject = "Confirm your email - P24 Agenda"
    message = render_to_string("logs/email_confirmation.html", {
        "name": myuser.first_name, 
        "domain": current_site.domain, 
        "uid": urlsafe_base64_encode(force_bytes(medecin.user.pk)),
        "token": generate_token.make_token(medecin)
        })
    
    email = EmailMessage(
        email_subject,
        message,
        settings.EMAIL_HOST_USER,
        [medecin.user.email],
    )

    email.fail_silently = True
    email.send()

def send_email_patient(request, mypatient):
    current_site = get_current_site(request)
    email_subject = "Your doctor " + request.user.last_name + " a activé votre compte - P24 Agenda."
    message = render_to_string("logs/email_confirmation.html", {
        "name": mypatient.user.first_name, 
        "domain": current_site.domain, 
        "uid": urlsafe_base64_encode(force_bytes(mypatient.user.pk)),
        "token": generate_token.make_token(mypatient)
        })
    
    email = EmailMessage(
        email_subject,
        message,
        settings.EMAIL_HOST_USER,
        [mypatient.user.email],
    )

    email.fail_silently = True
    email.send()

def send_email_justification(request, mypatient, slot):

    justification = request.POST.get('justification')
    current_site = get_current_site(request)
    email_subject = "Your doctor " + request.user.last_name + " a supprimé votre RDV !"
    message = render_to_string("accueil/email_suppression.html", {
        "name": mypatient.user.first_name, 
        "slot": slot,
        "justification": justification
        })
    
    email = EmailMessage(
        email_subject,
        message,
        settings.EMAIL_HOST_USER,
        [mypatient.user.email],
    )

    email.fail_silently = True
    email.send()
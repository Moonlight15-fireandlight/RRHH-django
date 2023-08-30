from app_rrhh.celery import app
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from celery import shared_task
from time import sleep
from django.core.mail import send_mail
from .models import *
from django.conf import settings


@shared_task()
def send_mail_task(email_address, message):
    sleep(10)
    email = EmailMessage(
        'Aurora app - renovacion de contrato',
        message,
        settings.EMAIL_HOST_USER,
        [email_address],
    )
    email.fail_silently=False
    email.send()

    return None

@shared_task()
def send_notification():
    try:
        empleados = Database.objects.filter(status="Por vencer").values().distinct()
        emails = []
        #names_boss = Database.objects.filter(bossmail=person, status="Por Vencer").values()
        for emp in empleados:
            emails.append(emp['bossmail'])
    
        emails_unit = list(set(emails)) #convierte el array en uno sin elementos repitivos
        for person in emails_unit:
            #email = EmailMessage(
            #    'Aurora app - renovacion de contrato',
            #    "Tiene contratos por renovar",
            #    settings.EMAIL_HOST_USER,
            #    [person],
            #)
            #email.fail_silently=False
            #email.send()
            names_boss = Database.objects.filter(bossmail=person, status="Por vencer").values().distinct()
            names = []
            for i in range(0,len(names_boss)):
                #names_boss = Database.objects.filter(bossmail=person, status="Por Vencer")   # resulta un queryset  
                #names_boss.values()
                names.append(names_boss[i]['name'])


            #message = "Tiene contrato por renovar de :" + " , ".join(names) 
            subject = "Aurora app - renovacion de contrato"
            message = "Tiene contrato por renovar de :" + " , ".join(names) 
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [person]
            send_mail(subject, message, email_from, recipient_list)
            #Enviar una notificacion de cada 2 dias a cada uno de los jefes que tengan empleados
            #con contratos por vencer
    except Exception as e:
        print(e)
        return None








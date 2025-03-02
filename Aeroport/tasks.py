import schedule
import time
import django
import os
from .models import CustomUser
from .models import BiletedeAvion
from django.core.mail import send_mail
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proiect1.settings')
django.setup()
from datetime import timedelta
from django.utils import timezone
import logging
logger=logging.getLogger('django')
def sterge_utilizatori_fara_email_confirmat():
    users=CustomUser.objects.filter(is_active=True, email_verified=False)
    for user in users:
        user.delete()
    logger.info("Utilizatorii fara email confirmat au fost stersi.")

def trimite_newsletter():
    users = CustomUser.objects.filter(date_joined__lte=timezone.now()-timedelta(days=1))
    for user in users:
        send_mail(
            'Newsletter',
            'Acesta este newsletter-ul nostru.',
            'noreply@gmail.com',
            ['rares.proiectdjango@gmail.com'],
            fail_silently=False,
        )
    logger.info(f"Newsletter trimis cu succes la {len(users)} utilizatori.")

def sterge_bilete_expirate():
    bilete=BiletedeAvion.objects.filter(data_plecare__lt=timezone.now())
    for bilet in bilete:
        bilet.delete()
    logger.info("Biletele expirate au fost sterse.")
        
def trimite_raport():
    new_users=CustomUser.objects.filter(date_joined__gte=timezone.now()-timedelta(days=7)).count()
    numar_bilete=BiletedeAvion.objects.filter(data_plecare__gte=timezone.now()-timedelta(days=7)).count()
    mesaj=f"In aceasta saptamana s-au inregistrat {new_users} utilizatori noi si s-au vandut {numar_bilete} bilete de avion."
    send_mail(
        'Raport saptamanal',
        mesaj,
        'rares.proiectdjango@gmail.com',
        ['rares.proiectdjango@gmail.com'],
        fail_silently=False,
    )
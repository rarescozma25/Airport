import schedule
import time
import django
import os
import sys
from Aeroport import tasks
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proiect1.settings')
django.setup()

def run_scheduler():
    schedule.every(2).minutes.do(tasks.sterge_utilizatori_fara_email_confirmat)
    schedule.every().monday.at("08:00").do(tasks.trimite_newsletter)
    schedule.every(1440).minutes.do(tasks.sterge_bilete_expirate) #in fiecare zi, sterge biletele cu data de plecare mai mica decat data curenta
    schedule.every().monday.at("08:00").do(tasks.trimite_raport)  #task-ul se va executa în fiecare luni la ora 8:00

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    try:
        run_scheduler()
    except KeyboardInterrupt:
        print("Scheduler oprit manual.")
        sys.exit()

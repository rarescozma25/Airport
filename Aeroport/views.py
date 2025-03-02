from django.shortcuts import render,redirect
from django.views.generic import ListView
from .models import Aeronava
from .models import CompanieAeriana
from .models import BiletedeAvion
from django.core.paginator import Paginator
from decimal import Decimal
from .forms import BiletFilterForm
from .forms import ContactForm
from .forms import ZborForm
from django.http import HttpResponse
from .forms import CustomUserCreationForm
from .forms import CustomAuthenticationForm
from django.contrib.auth import login
from datetime import datetime
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.core.mail import send_mail
from .models import CustomUser
import logging
logger = logging.getLogger('django')
def trimite_email():
    send_mail(
        subject='Salutare!',
        message='Salut. Ce mai faci?',
        html_message='<h1>Salut</h1><p>Ce mai faci?</p>',
        from_email='rares.proiectdjango@gmail.com',
        recipient_list=['rares.proiectdjango@gmail.com'],
        fail_silently=False,
    )

def index(request):
    trimite_email()
    logger.error('A apărut o eroare!')
class AvioaneViews(ListView):
    model = Aeronava
    template_name = 'avion.html'
    context_object_name = 'aeronave'

class CompanieAerianaViews(ListView):
    model = CompanieAeriana
    template_name = 'companie.html'
    context_object_name = 'companii'

def afisare_aeronave(request):
    aeronave = Aeronava.objects.filter(id_aeronava__lt=3)
    return render(request, 'avion.html', {'aeronave': aeronave})

def lista_bilete_avion(request):
    bilete = BiletedeAvion.objects.all()
    nume_prenume = request.GET.get('nume_prenume')
    pret_minim = request.GET.get('pret_minim')
    pret_maxim = request.GET.get('pret_maxim')
    loc=request.GET.get('loc')
    if nume_prenume:
        bilete=bilete.filter(nume_prenume__contains=nume_prenume) #
    if pret_minim:
        pret_minim = Decimal(pret_minim)
        bilete=bilete.filter(pret__gte=pret_minim)

    if pret_maxim:
        pret_maxim=Decimal(pret_maxim)
        bilete=bilete.filter(pret__lte=pret_maxim)
    if loc:
        bilete=bilete.filter(loc=loc)
    paginator=Paginator(bilete, 10)  
    page_number=request.GET.get('page')
    page_bilete=paginator.get_page(page_number)

    return render(request, 'lista_bilete_avion.html', {'bilete': page_bilete})
from django.http import HttpResponseForbidden
def lista_bilete_avion_form(request):
    bilete=BiletedeAvion.objects.all().order_by('id_bilet')
    form=BiletFilterForm(request.GET)
    
    if form.is_valid():
        nume_prenume = form.cleaned_data.get('nume_prenume')
        zbor_id = form.cleaned_data.get('zbor_id')
        pret_minim = form.cleaned_data.get('pret_minim')
        pret_maxim = form.cleaned_data.get('pret_maxim')
        loc = form.cleaned_data.get('loc')
        plecare = form.cleaned_data.get('plecare')
        destinatie = form.cleaned_data.get('destinatie')

        if nume_prenume:
            bilete = bilete.filter(nume_prenume__icontains=nume_prenume)
        if zbor_id:
            bilete = bilete.filter(zbor__id=zbor_id)
        if pret_minim is not None:
            bilete = bilete.filter(pret__gte=pret_minim)
        if pret_maxim is not None:
            bilete = bilete.filter(pret__lte=pret_maxim)
        if loc:
            bilete = bilete.filter(loc=loc)
        if plecare:
            bilete = bilete.filter(zbor__plecare__icontains=plecare)
        if destinatie:  
            bilete = bilete.filter(zbor__destinatie__icontains=destinatie)
    paginator=Paginator(bilete, 10)
    page_number=request.GET.get('page')
    page_bilete=paginator.get_page(page_number)
    if request.user.has_perm('Aeroport.view_biletedeavion'):
        return render(request, 'lista_bilete_avion_post.html', {'bilete': page_bilete, 'form': form})
    else:
        return HttpResponseForbidden(render(request, '403.html'))
def bilet(request, id_bilet): #pentru pagina care afiseaza un bilet cu id_bilet dat de mine
    bilet=get_object_or_404(BiletedeAvion, id_bilet=id_bilet)
    return render(request,'bilet.html',{'bilet': bilet})

def zbor(request, id_zbor):
    zbor = get_object_or_404(Zbor, id_zbor=id_zbor)
    return render(request, 'zbor.html', {'zbor': zbor})
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.salveaza_mesaj(cleaned_data=form.cleaned_data)
            return HttpResponse ("Mesajul a fost trimis cu succes!")
        else:
            logger.warning('Formularul de contact a fost completat greșit.')
            return render(request, 'contact.html', {'form': form})
    else:
        form=ContactForm()
        return render(request, 'contact.html', {'form': form})
        
def adauga_zbor(request):
    if request.method == 'POST':
        form = ZborForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponse("Zborul a fost adăugat cu succes!")
        else:
            return render(request, 'adauga_zbor.html', {'form': form})
    else:
        form = ZborForm()
        return render(request, 'adauga_zbor.html', {'form': form})
    
from django.core.mail import mail_admins
def register_view(request):
    messages.info(request, 'Creaza-ti un cont!')
    if request.method=='POST':
        form=CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            username=form.cleaned_data.get('username')
            email=form.cleaned_data.get('email')

            if username.lower()=='admin': #nu am voie cu username admin
                subject="Cineva încearcă să preia site-ul"
                context={'email': email}
                messages.warning(request,"Nu poti utiliza acest username.")

                html_message=render_to_string('alertapreluaresite.html', context) #trimitem mesaj la admini
                plain_message=f"Adresa de e-mail: {email}"
                mail_admins(subject, plain_message, html_message=html_message)

                messages.error(request,"Nu poți utiliza acest username.")
                return render(request,'inregistrare.html',{'form': form})

            form.save(request=request)
            messages.success(request,'Înregistrare realizată cu succes!')
            return redirect('login')

        else:
            messages.error(request,"Formular invalid. Verifică câmpurile completate.")
    
    else:
        form = CustomUserCreationForm()

    return render(request,'inregistrare.html',{'form': form})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import CustomAuthenticationForm

from django.shortcuts import render, redirect
from django.contrib.auth import login
from datetime import datetime
from django.contrib.auth import logout

from django.utils.timezone import now
from datetime import timedelta
failed_logins = {}
def custom_login_view(request):
    messages.info(request, 'Te rugam sa-ti introduci datele!')
    if request.method=='POST':
        form=CustomAuthenticationForm(data=request.POST, request=request)
        messages.debug(request, 'Formularul a fost completat.')
        try: #in caz ca nu putem obtine IP-ul
            username=request.POST.get('username', '')
            ip=get_client_ip(request)
        except:
            subject = "Eroare la obținerea IP-ului"
            plain_message="Nu s-a putut obține adresa IP."
            html_message=f"""
                <html>
                <body style="background-color: red; color: white;">
                    <h2>Eroare:{subject}</h2>
                    <p>{plain_message}</p>
                </body>
                </html>
            """
            mail_admins(subject, plain_message, html_message=html_message)

        if form.is_valid():
            user=form.get_user()
            if not user.email_confirmat: #utilizatorul nu si-a confirmat emailul
                logger.critical(f"Utilizatorul {user.username} nu și-a confirmat adresa de e-mail.")
                messages.error(request, 'Trebuie să îți confirmi adresa de e-mail înainte de a te autentifica.')
                return render(request, 'login.html', {'form': form})
            if user.blocat: #utilizatorul este blocat
                messages.error(request, 'Contul tau este blocat. Contacteaza un administrator.')
                return render(request, 'login.html', {'form': form})
                
            login(request, user)
            logger.info(f"Utilizatorul {user.username} s-a autentificat cu succes.")
            messages.success(request, 'Autentificare reusita!')

            if not form.cleaned_data.get('ramane_logat'): #daca nu a bifat "ramane logat"
                request.session.set_expiry(0) 
            else:
                request.session.set_expiry(24*60*60) #ramane logat pentru 24 de ore

            request.session["user_data"] = { #salvam datele utilizatorului in sesiune
                "username": user.username,
                "email": user.email,
                "telefon": user.telefon,
                "oras": user.oras,
                "tara": user.tara,
                "cod_postal": user.cod_postal,
                "data_nastere": user.data_nastere.isoformat() if user.data_nastere else None, #conversie din date in string
            }

            if username in failed_logins: #daca utilizatorul s-a autentificat cu succes, stergem incercarile nereusite
                del failed_logins[username]

            return redirect('home')
        else:
            logger.warning(f"Autentificare eșuată pentru utilizatorul {username} cu IP-ul {ip}.") 
            if username not in failed_logins: #daca utilizatorul nu a mai incercat sa se autentifice
                failed_logins[username] = []
            failed_logins[username].append({'ip': ip, 'timestamp': now()}) #adaugam incercarea nereusita

            failed_logins[username] = [
                log for log in failed_logins[username] if log['timestamp']>now()-timedelta(minutes=2)#stergem logurile mai vechi de 2 minute
            ]

            if len(failed_logins[username]) >= 3: #daca sunt mai mult de 3 incercari nereusite
                messages.warning(request, 'Nume de utilizator sau parola incorecta. Incearcă mai tarziu.')
                subject="Logări suspecte"
                context={
                    'username': username,
                    'ip': ip
                }
                html_message=render_to_string('logari_suspecte_email.html', context) #trimitem email la admini
                plain_message=f"Username: {username}\nIP: {ip}"
                mail_admins(subject, plain_message, html_message=html_message)
                logger.error(f"Utilizatorul {username} a încercat să se autentifice de mai multe ori.")

    else:
        form = CustomAuthenticationForm()

    return render(request, 'login.html', {'form': form})
def get_client_ip(request): #obtinem IP-ul utilizatorului
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR') #pentru a obtine IP-ul utilizatorului
    return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR') #returnam IP-ul utilizatorului

def home_view(request):
    if not request.user.is_authenticated: #daca utilizatorul nu este autentificat
        logger.debug("Utilizatorul nu este autentificat.")
        return redirect('login')
    
    user_data = request.session.get("user_data", None) #obtinem datele utilizatorului din sesiune
    if user_data:
        if user_data.get("data_nastere"):
            user_data["data_nastere"]=datetime.strptime(user_data["data_nastere"], '%Y-%m-%d').date() #conversie din string in date
        
        context={'user_data': user_data} #trimitem datele utilizatorului in context
    else:
        context = {}

    return render(request,'home.html', context) #afisam pagina home.html


def logout_view(request): #pentru a face logout
    logout(request)
    return redirect('login')

def change_password_view(request):
    messages.debug(request, 'Schimba-ti parola!')
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Parola a fost actualizata')
            logger.info(f"Utilizatorul {request.user.username} a schimbat parola.")
            return redirect('home')
        else:
            messages.error(request, 'Exista erori.')
            logger.error(f"Utilizatorul {request.user.username} a introdus o parola invalida.")
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'schimba_parola.html', {'form': form})

def confirma_mail(request, cod):
    user=get_object_or_404(CustomUser, cod=cod)

    if user.email_confirmat:
        logger.debug(f"Utilizatorul {user.username} a incercat sa confirme un email deja confirmat.")
        return HttpResponse("Emailul este deja confirmat.")
        
    
    user.email_confirmat=True
    user.save()

    return HttpResponse(f"Mulțumim, {user.first_name}! Emailul tau a fost confirmat cu succes.")
from django.contrib.auth.decorators import login_required
from .models import Zbor
from .forms import CautaZborForm
from django.shortcuts import render
from .models import Zbor, Vizualizare
from django.contrib.auth.decorators import login_required
from .forms import CautaZborForm
from django.utils import timezone
def cauta_zboruri_view(request):
    zboruri=None
    
    if request.method == 'POST':
        form = CautaZborForm(request.POST)
        if form.is_valid():
            destinatie = form.cleaned_data['destinatie']
            zboruri = Zbor.objects.filter(destinatie__icontains=destinatie)

            for zbor in zboruri:
                if not Vizualizare.objects.filter(user=request.user, zbor=zbor).exists():
                    vizualizare = Vizualizare(
                        user=request.user,
                        zbor=zbor, 
                        data_vizualizare=timezone.now()
                    )
                    vizualizare.save()

            vizualizari = Vizualizare.objects.filter(user=request.user, zbor__destinatie=destinatie)
            if vizualizari.count() >= 2:
                logger.debug(f"Utilizatorul {request.user.username} este eligibil pentru promoția pentru {destinatie}!")

    else:
        form = CautaZborForm()

    return render(request, 'lista_zboruri.html', {'form': form, 'zboruri': zboruri})




from django.core.mail import send_mass_mail, EmailMessage
from django.template.loader import render_to_string
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PromotieForm
from .models import Promotie, CustomUser, Vizualizare

@login_required
def creare_promotie_view(request):
    if request.method == 'POST':
        form = PromotieForm(request.POST)
        if form.is_valid():
            promotie = form.save()
            utilizatori_promotie = []
            for utilizator in CustomUser.objects.all():
                vizualizari = Vizualizare.objects.filter(user=utilizator, zbor__destinatie=promotie.destinatie)

                if vizualizari.count() >= 2:
                    utilizatori_promotie.append(utilizator)

            email_list = []
            for utilizator in utilizatori_promotie:
                subject = promotie.subiect
                html_message = render_to_string('email_promotie.html', {
                    'promotie': promotie, 
                    'utilizator': utilizator
                })

                email = EmailMessage(
                    subject,  
                    html_message,  
                    'noreply@gmail.com',
                    ['rares.proiectdjango@gmail.com'], 
                    logger.debug(f"Email trimis cu succes către {utilizator.email}.")
                )

                email.content_subtype = "html"  
                email_list.append(email)  

            send_mass_mail([(email.subject, email.body, email.from_email, email.to) for email in email_list], fail_silently=False) #nu are html

            return redirect('promotie')  

    else:
        form = PromotieForm()

    return render(request, 'creare_promotie.html', {'form': form})
from .forms import AdaugaBileteForm

from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import AdaugaBileteForm

def adauga_bilete_avion(request):
    if not request.user.is_authenticated:
        return render(request, '403.html', {
            'titlu': "Eroare autentificare",
            'mesaj_personalizat': "Trebuie să fii autentificat pentru a accesa această resursă."
        }, status=403)

    if not request.user.has_perm('Aeroport.add_biletedeavion'):
        return render(request, '403.html', {
            'titlu': "Eroare adăugare bilete",
            'mesaj_personalizat': "Nu ai voie să adaugi bilete."
        }, status=403)
    if request.method == 'POST':
        form = AdaugaBileteForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('<p style="color: green;">Biletul a fost adăugat cu succes!</p>')
        else:
            return render(request, 'adauga_bilet.html', {'form': form})
    else:
        form = AdaugaBileteForm()
        return render(request, 'adauga_bilet.html', {'form': form})


def lista_zboruri(request):
    zboruri_list = Zbor.objects.all().order_by('id_zbor')
    paginator = Paginator(zboruri_list, 10)
    page_number = request.GET.get('page')
    zboruri = paginator.get_page(page_number)
    return render(request, 'zboruri_lista.html', {'zboruri': zboruri})
import json
def cos_virtual(request):
    zboruri=Zbor.objects.all()
    zboruri_json = [
        {
            'id': zbor.id_zbor,
            'plecare': zbor.plecare,
            'destinatie': zbor.destinatie,
            'pret': float(zbor.pret),
        }
        for zbor in zboruri
    ]
    return render(request, 'afiseaza_cos.html', {'zboruri_json': json.dumps(zboruri_json)})          
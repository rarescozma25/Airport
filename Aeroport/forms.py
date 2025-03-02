from django import forms
from datetime import date,timedelta,datetime
from .models import Zbor
from .models import Aeronava
from django.contrib.auth.forms import PasswordChangeForm
import re
import os
import json
import time
from django.conf import settings
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
import logging
logger = logging.getLogger('django')
class BiletFilterForm(forms.Form):
    nume_prenume = forms.CharField(required=False, label="Nume Prenume")
    pret_minim = forms.DecimalField(required=False, label="Preț Minim", min_value=0)
    pret_maxim = forms.DecimalField(required=False, label="Preț Maxim", min_value=0)
    loc = forms.CharField(required=False, label="Loc")
    plecare = forms.CharField(required=False, label="Loc de Plecare")
    destinatie = forms.CharField(required=False, label="Destinație")
from .models import BiletedeAvion
class AdaugaBileteForm(forms.Form):
    nume_prenume = forms.CharField(required=True, label="Nume Prenume")
    pret = forms.DecimalField(required=True, label="Preț", min_value=0)
    loc = forms.CharField(required=True, label="Loc")
    zbor = forms.ModelChoiceField(queryset=Zbor.objects.all(), required=True, label="Zbor")

    def save(self):
        nume_prenume = self.cleaned_data['nume_prenume']
        pret = self.cleaned_data['pret']
        loc = self.cleaned_data['loc']
        zbor = self.cleaned_data['zbor']
        bilet = BiletedeAvion(nume_prenume=nume_prenume, pret=pret, loc=loc, zbor=zbor)
        bilet.save()
            
class ContactForm(forms.Form):
    nume=forms.CharField(max_length=10,required=True,label="Nume")
    prenume=forms.CharField(max_length=10,required=False,label="Prenume")
    data_nasterii=forms.DateField(required=False,label="Data Nasterii",
                                  help_text="YYYY-MM-DD",
                                  error_messages={'requiered':"YYYY-MM-DD"})
    email=forms.EmailField(required=True,label="Email")
    confirmare_email=forms.EmailField(required=True,label="Confirmare Email")
    tip_mesaj = forms.ChoiceField(choices=[('reclamatie', 'Reclamație'), ('intrebare', 'Întrebare'), 
                                           ('review', 'Review'), ('cerere', 'Cerere'), 
                                           ('programare', 'Programare')], required=False, label="Tip Mesaj")
    subiect=forms.CharField(max_length=100,required=True,label="Subiect")
    min_zile_asteptare=forms.IntegerField(min_value=1,required=False,label="Minim Zile Așteptare")
    mesaj=forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}), 
        required=True, 
        label="Mesaj (Semnați cu numele dvs. la final)",
        error_messages={'required':'Mesajul este obligatoriu'},
        help_text="Introduceti mesajul dumneavoastra")
    
    def salveaza_mesaj(self,cleaned_data):
        timestamp=int(time.time())
        cleaned_data.pop('confirmare_email',None)
        cleaned_data.pop('data_nasterii',None)
        nume_fisier=f"mesaj_{timestamp}.json"
        folder=os.path.join(settings.BASE_DIR,"mesaje")
        if not os.path.exists(folder):
            os.makedirs(folder)
        cale_fisier=os.path.join(folder,nume_fisier)
        with open(cale_fisier,"w") as fisier:
            json.dump(cleaned_data,fisier)
    
    def clean(self):
        #validarea nume,prenume subiect
        def verificare_text(text):
            return text[0].isupper() and text.isalpha()
        
        
        cleaned_data=super().clean()
        #validare nume
        nume=cleaned_data.get('nume')
        if not verificare_text(nume):
            raise forms.ValidationError("Numele trebuie sa inceapa cu litera mare si sa contina doar litere")
        if nume=="Admin":
            logger.critical("Numele nu poate fi Admin")
        #validare prenume
        prenume=cleaned_data.get('prenume')
        if prenume:
            if not verificare_text(prenume):
                raise forms.ValidationError("Prenumele trebuie sa inceapa cu litera mare si sa contina doar litere")
        #validare email
        email=cleaned_data.get('email')
        confirmare_email=cleaned_data.get('confirmare_email')
        if email!=confirmare_email and email and confirmare_email:
            raise forms.ValidationError("Email-urile nu coincid")
        
        tip_mesaj=cleaned_data.get('tip_mesaj')
        #validare subiect
        subiect=cleaned_data.get('subiect')
        if not verificare_text(subiect):
            raise forms.ValidationError("Subiectul trebuie sa inceapa cu litera mare si sa contina doar litere")
        
        min_zile_asteptare=cleaned_data.get('min_zile_asteptare')
        
        mesaj=cleaned_data.get('mesaj')
        mesaj=re.sub(r'\s+', ' ', mesaj.replace('\n', ' ')).strip()
        #validare mesaj
        def validare_mesaj(mesaj):
            cuvinte=re.findall(r'\b\w+\b',mesaj)
            lungime=len(cuvinte)
            if lungime<5 or lungime>100:
                return False
            for cuv in cuvinte:
                if cuv.lower().startswith("https://") or cuv.lower().startswith("http://"):
                    return False
            return True
        
        if not validare_mesaj(mesaj):
            raise forms.ValidationError("Mesajul trebuie sa inceapa cu litera mare si sa respecte numarul de caractere")
        cleaned_data['mesaj']=mesaj
        semnatura_mesaj=mesaj.split()[-1] if not prenume else " ".join(mesaj.split()[-2:])
        nume_complet_utilizator=f"{nume} {prenume}".strip() if prenume else nume.strip()
    
        if semnatura_mesaj.lower()!=nume_complet_utilizator.lower():
            raise forms.ValidationError(
                f"Semnătura mesajului trebuie să fie numele complet al utilizatorului: „{nume_complet_utilizator}”."
            )
        return cleaned_data
        
    def calculate_age(self,data_nasterii): #calculam varsta
        today=date.today() 
        years=today.year-data_nasterii.year
        months=today.month-data_nasterii.month
        if months<0:
            years-=1
            months+=12
        return years
    def is_valid(self):
        is_valid = super().is_valid()
        if is_valid:
            self.salveaza_mesaj(self.cleaned_data)
        return is_valid
    
    def clean_data_nasterii(self): #validare data nasterii
        data_nasterii=self.cleaned_data['data_nasterii']
        if data_nasterii>date.today():
            raise forms.ValidationError("Data nasterii nu poate fi in viitor")
        varsta=self.calculate_age(data_nasterii)
        if varsta<18:
            raise forms.ValidationError("Trebuie să aveți minim 18 ani pentru a trimite un mesaj")
        self.cleaned_data['varsta']=varsta
    
class ZborForm(forms.ModelForm):
    #campuri pe care nu le avem in model
    durata_zbor=forms.DurationField(
         required=True,
         label="Durata Zbor",
         help_text="Introduceti durata zborului in format hh:mm:ss",
         error_messages={'required': 'Durata zborului este obligatorie','invalid':'Durata zborului trebuie sa fie in format hh:mm:ss'}                           
                                    )
    tip_zbor=forms.ChoiceField(
        required=True,
        label="Tip Zbor",
        choices=[('intern','Intern'),('extern','Extern')],
        help_text="Selectati tipul zborului",
        error_messages={'required': 'Tipul zborului este obligatoriu'}
    )
    aeronava=forms.ModelChoiceField(
        queryset=Aeronava.objects.all(),
        required=True,
        label="Aeronava",
        help_text="Selectati aeronava",
        error_messages={'required': 'Aeronava este obligatorie'}
    )
    class Meta:
        model=Zbor
        fields=['plecare','destinatie','data_plecare','ora_plecare']
        labels={'plecare':'Loc de plecare','destinatie':'Destinatie','data_plecare':'Data plecare','ora_plecare':'Ora plecare'}
        help_text={
            'required':'Toate campurile sunt obligatorii',
            'plecare':'Introduceti locul de plecare',
            'destinatie':'Introduceti destinatia',
            'data_plecare':'Introduceti data plecarii',
            'ora_plecare':'Introduceti ora plecarii',
        }
        error_messages={
            'plecare':{ 'required':'Locul de plecare este obligatoriu',
                       'max_length':'Locul de plecare nu poate avea mai mult de 50 caractere'}, 
            'destinatie':{ 'required':'Destinatia este obligatorie',
                       'max_length':'Destinatia nu poate avea mai mult de 50 caractere'},
            'data_plecare':{ 'required':'Data plecarii este obligatorie',
                                'invalid':'Data plecarii trebuie sa fie in formatul yyyy-mm-dd'},
            'ora_plecare':{ 'required':'Ora plecarii este obligatorie',
                           'invalid':'Ora plecarii trebuie sa fie in formatul hh:mm:ss'}
        }
    def clean_dataplecare(self): #validare data plecare
        data_plecare=self.cleaned_data['data_plecare']
        if data_plecare is None:
            raise forms.ValidationError("Data plecarii este obligatorie")
        if data_plecare<date.today():
            raise forms.ValidationError("Data plecarii nu poate fi in trecut")
        return data_plecare
    def clean_duratazbor(self): #validare durata zbor
        durata_zbor=self.cleaned_data['durata_zbor']
        if durata_zbor is None:
            raise forms.ValidationError("Durata zborului este obligatorie")
        if durata_zbor< timedelta(minutes=30):
            raise forms.ValidationError("Durata zborului nu poate fi mai mica de 30 de minute")
        return durata_zbor
    def clean(self):
        cleaned_data=super().clean()
        plecare=cleaned_data.get('plecare')
        destinatie=cleaned_data.get('destinatie') #validare plecare si destinatie
        if destinatie is None:
            raise forms.ValidationError("Destinatia este obligatorie")
        if plecare is None:
            raise forms.ValidationError("Locul de plecare este obligatoriu")
        if plecare.lower()==destinatie.lower():
            raise forms.ValidationError("Locul de plecare si destinatia nu pot fi aceleasi")
        return cleaned_data
    def save(self,commit=False):
        zbor=super().save(commit=False)
        durata_zbor=self.cleaned_data['durata_zbor']
        tip_zbor=self.cleaned_data['tip_zbor']
        durata_suplimentara=timedelta(minutes=30) if tip_zbor=='extern' else timedelta() #daca zborul este extern, durata suplimentara este de 30 de minute
        ora_plecare=zbor.ora_plecare 
        plecare_zbor=datetime.combine(zbor.data_plecare,ora_plecare)
        sosire_zbor=plecare_zbor+durata_zbor+durata_suplimentara
        zbor.data_sosire=sosire_zbor.date()
        zbor.ora_sosire=sosire_zbor.time()
        zbor.aeronava_id=self.cleaned_data['aeronava'].id_aeronava
        if commit:
            zbor.save()


from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.crypto import get_random_string
from django.contrib.sites.shortcuts import get_current_site




class CustomUserCreationForm(UserCreationForm): #formular pentru a crea un user
    telefon=forms.CharField(required=True)
    data_nastere=forms.DateField(required=True) 
    oras=forms.CharField(required=True)
    tara=forms.CharField(required=True)
    cod_postal=forms.CharField(required=True)

    class Meta:
        model=CustomUser
        fields=("username","email","telefon","password1","password2","data_nastere","oras","tara","cod_postal")

    def clean_telefon(self): #validare telefon
        telefon=self.cleaned_data.get("telefon")
        if not telefon.isdigit():
            raise forms.ValidationError("Numarul de telefon trebuie sa conțina doar cifre.")
        if len(telefon)<10 or len(telefon)>15:
            raise forms.ValidationError("Numarul de telefon trebuie sa aiba între 10 si 15 cifre.")
        return telefon

    def clean_data_nastere(self): #validare data nasterii
        data_nastere = self.cleaned_data.get("data_nastere")
        from datetime import date
        today=date.today()
        age=today.year-data_nastere.year-((today.month,today.day)<(data_nastere.month,data_nastere.day))
        if age<18:
            raise forms.ValidationError("Trebuie sa aveți cel putin 18 ani pentru a va inregistra.")
        return data_nastere

    def clean_cod_postal(self): #validare cod postal
        cod_postal=self.cleaned_data.get("cod_postal")
        if not cod_postal.isdigit():
            raise forms.ValidationError("Codul postal trebuie sa contina doar cifre.")
        if len(cod_postal)!=6:
            raise forms.ValidationError("Codul poștal trebuie sa aiba exact 6 cifre.")
        return cod_postal

    def save(self, request, commit=True): #salvare user
        user=super().save(commit=False) #cleaned_data reprezinta un dictionar cu datele valide introduse in formular
        user.telefon=self.cleaned_data["telefon"]
        user.data_nastere=self.cleaned_data["data_nastere"]
        user.oras=self.cleaned_data["oras"]
        user.tara=self.cleaned_data["tara"]
        user.cod_postal=self.cleaned_data["cod_postal"]
        user.cod=get_random_string(length=10)
        user.email_confirmat=False
        if commit:
            user.save()
            self.trimite_mail(user, request)
        return user

    def trimite_mail(self, user, request):
        from django.contrib.sites.shortcuts import get_current_site
        from django.core.mail import EmailMessage
        from django.template.loader import render_to_string

        domain=get_current_site(request).domain
        link_confirmare=f'http://{domain}/confirma_mail/{user.cod}/'
        context={
            'username':user.username,
            'link_confirmare':link_confirmare
        }

        html_content=render_to_string('email_template.html',context)

        email = EmailMessage(
            subject='Bun venit!',
            body=html_content,
            from_email='noreply@domeniu.com',
            to=['rares.proiectdjango@gmail.com'],
        )
        email.content_subtype='html'
        email.html_message=html_content
        email.send(fail_silently=False)

    

class CustomAuthenticationForm(AuthenticationForm): #formular pentru login
    ramane_logat=forms.BooleanField( #checkbox pentru a ramane logat
        required=False,
        initial=False,
        label='Ramaneti logat'
    )

    def clean(self):        
        cleaned_data=super().clean()
        ramane_logat=self.cleaned_data.get('ramane_logat')
        return cleaned_data

class CustomPasswordChangeForm(PasswordChangeForm):
    def clean_new_password1(self):
        password1=self.cleaned_data.get('new_password1')
        if len(password1)<10:
            raise forms.ValidationError("Parola trebuie sa aiba macar 10 caractere.")
        return password1


#email rares.proiectdjango@gmail.com parola:rares12345
from .models import Promotie
class CautaZborForm(forms.Form):
    destinatie = forms.CharField(label='Destinația', max_length=100, required=True)
    
    
class PromotieForm(forms.ModelForm):
    destinatie = forms.CharField(max_length=100)
    subiect = forms.CharField(max_length=200)
    data_expirare = forms.DateTimeField()
    procent_reducere = forms.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        model = Promotie
        fields = ['nume', 'subiect', 'data_expirare', 'procent_reducere', 'destinatie']

    def save(self, commit=True): 
        instance = super().save(commit=False) #chem metoda save din clasa parinte super
        if commit: #daca commit este True, salveaza in baza de date
            instance.save()
        return instance

from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.utils import timezone

#tipuri de date folosite: CharField, DateField, EmailField, URLField, PositiveIntegerField, BooleanField, TimeField, DecimalField, ManyToManyField, ForeignKey
class CompanieAeriana(models.Model):
    id_companie=models.AutoField(primary_key=True)
    nume_companii=[('Tarom', 'Tarom'), ('BlueAir', 'BlueAir'), 
                   ('WizzAir', 'WizzAir'), ('RyanAir', 'RyanAir'), 
                   ('Lufthansa', 'Lufthansa'), ('TurkishAirlines', 'TurkishAirlines'),
                   ('AirFrance', 'AirFrance'), ('Qatar', 'Qatar')]
    nume=models.CharField(max_length=50, choices=nume_companii)
    an_infiintare=models.DateField()
    email=models.EmailField()
    sediu=models.CharField(max_length=50)
    website=models.URLField()
    def __str__(self):
        return self.nume

class Aeronava (models.Model):
    id_aeronava=models.AutoField(primary_key=True)
    nume=models.CharField(max_length=50)
    capacitate=models.PositiveIntegerField()
    an_fabricatie=models.DateField()
    disponibilitate=models.BooleanField()
    companie_aeriana=models.ForeignKey(CompanieAeriana, on_delete=models.CASCADE)
    def __str__(self):
        return self.nume
from django.urls import reverse
class Zbor(models.Model):
    id_zbor=models.AutoField(primary_key=True)
    plecare=models.CharField(max_length=50)
    destinatie=models.CharField(max_length=50)
    data_plecare=models.DateField()
    ora_plecare=models.TimeField()
    data_sosire=models.DateField()
    ora_sosire=models.TimeField()
    pret=models.DecimalField(max_digits=7, decimal_places=2,default=0)
    aeronava=models.ForeignKey(Aeronava, on_delete=models.CASCADE)
    actualizat_la = models.DateField(auto_now=True)
    def get_absolute_url(self):
        return reverse('carte', kwargs={'id': self.id})
    def __str__(self):
        return self.plecare + ' ' + self.destinatie

class BiletedeAvion(models.Model):
    id_bilet=models.AutoField(primary_key=True)
    nume_prenume=models.CharField(max_length=50)
    zbor=models.ForeignKey(Zbor, on_delete=models.CASCADE)
    pret=models.DecimalField(max_digits=7, decimal_places=2)
    loc=models.CharField(max_length=10)
    actualizat_la = models.DateField(auto_now=True)
    def get_absolute_url(self):
        return reverse('carte', kwargs={'id': self.id})


class Rezervare(models.Model):
    id_rezervare=models.AutoField(primary_key=True)
    zbor=models.ForeignKey(Zbor, on_delete=models.CASCADE)
    status=models.BooleanField() #True=procesat False=neprocesat
    data_rezervare=models.DateField()


class EchipajdeBord(models.Model):
    id_echipaj=models.AutoField(primary_key=True)
    nume=models.CharField(max_length=50)
    data_nastere=models.DateField()
    prenume=models.CharField(max_length=50)
    tipuri_functii = [
        ('pilot', 'Pilot'),
        ('copilot', 'Copilot'),
        ('insotitor', 'Insotitor de zbor')
    ]
    functie=models.CharField(max_length=50, choices=tipuri_functii)
    zbor=models.ManyToManyField(Zbor)
    companieaeriana=models.ForeignKey(CompanieAeriana, on_delete=models.CASCADE)
    
class CustomUser(AbstractUser): #implicit are campurile: username, email, password
    telefon = models.CharField(max_length=15, blank=True)
    tara=models.CharField(max_length=50, blank=True)
    oras=models.CharField(max_length=50, blank=True)
    data_nastere=models.DateField(blank=True,null=True)
    cod_postal=models.CharField(max_length=20, blank=True)
    cod = models.CharField(max_length=100, null=True, blank=True)
    email_confirmat = models.BooleanField(default=False)
    blocat=models.BooleanField(default=False,)
    
    
class Promotie(models.Model):
    nume=models.CharField(max_length=100)
    subiect=models.CharField(max_length=200)
    data_expirare=models.DateTimeField()
    procent_reducere=models.DecimalField(max_digits=5, decimal_places=2)
    destinatie=models.CharField(max_length=100,default="Unknown")
    def __str__(self):
        return self.nume

class Vizualizare(models.Model):
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    zbor=models.ForeignKey(Zbor,on_delete=models.CASCADE,default=None) 
    data_vizualizare = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-data_vizualizare']




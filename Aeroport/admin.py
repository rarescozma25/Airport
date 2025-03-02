from django.contrib import admin

# Register your models here.
from .models import Aeronava
from .models import CompanieAeriana
from .models import Zbor
from .models import BiletedeAvion
from .models import Rezervare
from .models import EchipajdeBord
from .models import CustomUser

admin.site.site_header = 'Administrare Aeroport'
admin.site.index_title = "Gestionarea Datelor de Zbor și Echipaj"

class AeronavaAdmin(admin.ModelAdmin):
    list_display = ('nume', 'capacitate', 'an_fabricatie', 'disponibilitate', 'companie_aeriana')  # am schimbat ordinea campurilor
    list_filter = ('nume', 'companie_aeriana')
    search_fields = ('nume', 'companie_aeriana') #cautare
    ordering = ['nume']
    fieldsets = ( #se poate observa atunci cand adaugam o aeronava
        ('Detalii generale', {
            'fields': ('nume','companie_aeriana')
        }),
        ('Detalii suplimentare', {
            'fields': ('an_fabricatie', 'disponibilitate', 'capacitate')
        }),
    )

admin.site.register(Aeronava, AeronavaAdmin)
class RezervareAdmin(admin.ModelAdmin):
    list_display = ('data_rezervare', 'zbor', 'status')  # am schimbat ordinea campurilor
    search_fields = ('zbor__plecare', 'zbor__destinatie') #cautare
    fields = ('zbor', 'data_rezervare', 'status')
admin.site.register(Rezervare,RezervareAdmin)

class CompanieAerianaAdmin(admin.ModelAdmin):
    list_display = ('nume','email', 'sediu', 'website','an_infiintare')
    list_filter = ('nume',)
    search_fields = ('nume',) #cautare
    ordering = ['nume']
    fields = ('nume', 'sediu','email' , 'website','an_infiintare')
admin.site.register(CompanieAeriana, CompanieAerianaAdmin)

class EchipajdeBordAdmin(admin.ModelAdmin):
    list_display = ('nume', 'prenume','functie','companieaeriana')
    list_filter = ('companieaeriana',)
    search_fields = ('nume', 'prenume') #cautare
    ordering = ['nume']

admin.site.register(EchipajdeBord,EchipajdeBordAdmin)

class ZborAdmin(admin.ModelAdmin):
    list_display = ('plecare', 'destinatie', 'data_plecare', 'data_sosire','ora_plecare', 'ora_sosire','aeronava','pret')
    list_filter = ('plecare', 'destinatie')
    search_fields = ('plecare', 'destinatie')
    ordering = ['plecare', 'destinatie']
    fields = ('plecare', 'destinatie', 'data_plecare', 'data_sosire','ora_plecare', 'ora_sosire','aeronava','pret')
admin.site.register(Zbor, ZborAdmin)

class BiletedeAvionAdmin(admin.ModelAdmin):
    list_display = ('nume_prenume', 'zbor', 'pret', 'loc')
    list_filter = ('nume_prenume', 'zbor')
    search_fields = ('nume_prenume', 'zbor')
    ordering = ['nume_prenume', 'zbor']
    fields = ('nume_prenume', 'zbor', 'pret', 'loc')
    
admin.site.register(BiletedeAvion, BiletedeAvionAdmin)
from django.contrib.auth.admin import UserAdmin
class CustomUserAdmin(UserAdmin):
    model=CustomUser
    search_fields = ('email', 'username')
    fieldsets = UserAdmin.fieldsets+(
        (None, {'fields': ('telefon','cod_postal','oras','data_nastere','tara','blocat')}),
    )
admin.site.register(CustomUser, CustomUserAdmin)
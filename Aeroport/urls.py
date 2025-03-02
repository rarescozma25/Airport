from django.urls import path
from . import views
from .views import AvioaneViews
from .sitemaps import ZborSitemap, BiletSitemap, VederiStaticeSitemap

sitemaps={
    'zboruri':ZborSitemap,
    'bilete':BiletSitemap,
    'static':VederiStaticeSitemap
}


urlpatterns = [
    path('avioane/', AvioaneViews.as_view(), name='avioane_list'),
    path('afisare_aeronave/', views.afisare_aeronave, name='afisare_aeronave'),
    path('bilete/', views.lista_bilete_avion, name='lista_bilete_avion'),
    path('bilete_form/', views.lista_bilete_avion_form, name='lista_bilete_avion_form'),
    path('bilet/<int:id_bilet>', views.bilet, name='lista_bilete_avion_form'),
    path('zbor/<int:id_zbor>/', views.zbor, name='detalii_zbor'),
    path('contact/', views.contact, name='contact'),
    path('adauga_zbor/',views.adauga_zbor,name='adauga_zbor'),
    path ('registeruser/',views.register_view,name='registeruser'),
    path('login/',views.custom_login_view,name='login'),
    path('', views.home_view, name='home'), 
    path('schimba_parola/', views.change_password_view, name='schimba_parola'),
    path('index/', views.index, name='index'),
    path('confirma_mail/<str:cod>/', views.confirma_mail, name='confirma_mail'),
    path('cauta_zboruri/', views.cauta_zboruri_view, name='cauta_zboruri'),
    path('promotii/', views.creare_promotie_view, name='promotie'),
    path('adauga_bilet/',views.adauga_bilete_avion,name='adauga_bilet'),
    path('logout/',views.logout_view,name='logout'),
    path('home/',views.home_view,name='home'),
    path('zboruri/',views.lista_zboruri,name='zboruri'),
    path('cos_virtual/', views.cos_virtual, name='cos_virtual'),
    #path('sitemap.xml', sitemaps, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]



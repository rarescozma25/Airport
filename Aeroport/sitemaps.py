from django.contrib.sitemaps import Sitemap
from .models import Zbor, BiletedeAvion

class ZborSitemap(Sitemap):
    changefreq = "monthly"
    priority=0.5
    def items(self):
        return Zbor.objects.all()
    def lastmod(self, obj):
        return obj.actualizat_la

class BiletSitemap(Sitemap):
    changefreq="monthly"
    priority = 0.5
    def items(self):
        return BiletedeAvion.objects.all()

    def lastmod(self, obj):
        return obj.actualizat_la
from django.urls import reverse
class VederiStaticeSitemap(Sitemap): #pagini statice=cele care nu sufera modificari si nu depind de logarea utilizatorului
    changefreq="monthly"
    priority=0.5

    def items(self):
        return ['index','contact','registeruser','login','zboruri','cost_virtual']

    def location(self, item):
        return reverse(item)

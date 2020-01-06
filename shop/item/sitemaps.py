from django.contrib.sitemaps import Sitemap 
from .models import Item, ItemCategory


class ItemSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 1
    protocol = 'https'
    i18n = True 

    def items(self):
        return Item.objects.all()
        
    def lastmod(self, obj):
        return obj.updated


class CategorySitemap(Sitemap):
    changefreq = 'never'
    priority = 1
    protocol = 'https'
    i18n = True

    def items(self):
        return ItemCategory.objects.all()

    def lastmod(self, obj):
        return obj.updated


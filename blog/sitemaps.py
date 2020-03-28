from django.contrib.sitemaps import Sitemap 
from django.shortcuts import  reverse 

from .models import Post, PostCategory



class PostSitemap(Sitemap):
    i18n = True
    changefreq = 'weekly' 
    protocol = 'https'
    priority = 1

    def items(self):
        return Post.objects.all()
        
    def location(self, obj):
        return obj.get_absolute_url()

    def lastmod(self, obj):
        return obj.updated


class PostCategorySitemap(Sitemap):
    changefreq = 'weekly' # never| 
    protocol = 'https'
    i18n = True 
    priority = 1

    def items(self):
        return PostCategory.objects.all()
        
    def location(self, obj):
        return obj.get_absolute_url()

    def lastmod(self, obj):
        return obj.updated


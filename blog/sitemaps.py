from django.contrib.sitemaps import Sitemap 
from box.blog.models import Post 
from django.shortcuts import  reverse 


class PostViewSitemap(Sitemap):
    i18n = True
    changefreq = 'weekly' 
    protocol = 'https'

    def items(self):
        return Post.objects.all()
        
    def location(self, item):
        return reverse(item)




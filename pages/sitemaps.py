from django.contrib.sitemaps import Sitemap 
from blog.models import Post 
from django.urls import reverse 


class StaticViewSitemap(Sitemap):

    def items(self):
        return [
            "index",
            "services",
            "about",
            "contacts",
            "thank_you",
        ]
        
    def location(self, item):
        return reverse(item)




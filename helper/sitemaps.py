from django.contrib.sitemaps import Sitemap 
from django.urls import reverse 
from .models import * 



class StaticChatSitemap(Sitemap):

    def items(self):
        return [
            #список назв статичних сторінок з project.urls.static_urls
            "index",
            "services",
            "about",
            "contacts",
            "profile",
            "thank_you",
            "basket",
            "search",
            "blog",
        ]
        
    def location(self, item):
        return reverse(item)




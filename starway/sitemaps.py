from django.contrib.sitemaps import Sitemap 
from django.urls import reverse 
from .models import * 



class StaticChatSitemap(Sitemap):

    def items(self):
        return [
            "starway_index",
            "starway_contacts",
            "starway_profile",
            "starway_service_categories",
            "starway_case_categories",
            "starway_about",
            "starway_how_it_works",
            "starway_story",
            "starway_team",
            "starway_become_member",
        ]
        
    def location(self, item):
        return reverse(item)




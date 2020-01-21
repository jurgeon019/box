from django.contrib.sitemaps import Sitemap 
from .models import Post 



class PostSitemap(Sitemap):
    i18n = True
    changefreq = 'weekly' 
    protocol = 'https'

    def items(self):
        return Post.objects.all()
        
    def location(self, item):
        # return reverse(item)
        return item.get_absolute_url()




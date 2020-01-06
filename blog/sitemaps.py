from django.contrib.sitemaps import Sitemap 
from blog.models import Post 



class PostViewSitemap(Sitemap):
    i18n = True
    changefreq = 'weekly' 
    protocol = 'https'

    def items(self):
        return Post.objects.all()
        
    def location(self, item):
        return reverse(item)




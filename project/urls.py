from django.urls import path, include


from filebrowser.sites import site

from django.contrib import admin
from project.admin import custom_admin
from project.views import *
from project.utils import *

from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import JavaScriptCatalog as js_cat

from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView as t_v

from shop.item.sitemaps import *
from blog.sitemaps import *
from pages.sitemaps import *



sitemaps = {
  'items': ItemSitemap,
  'categories': CategorySitemap,
  'posts': PostViewSitemap, 
  'static':StaticViewSitemap,
}


handler404 = 'project.views.handler_404'
handler500 = 'project.views.handler_500'

urlpatterns = []


multilingual_urls = [
  path('accounts/', include('allauth.urls')),
  path('test/', include('shop.test_shop.urls')),
  path('', include('shop.order.urls')),
  path('', include('shop.liqpay.urls')),
  path('', include('custom_admin.urls')),
  path('', include('pages.urls')),
  path('', include('forms.urls')),
]

urlpatterns += [
  path('', include(multilingual_urls))
]
# urlpatterns += i18n_patterns(
#   path('', include(multilingual_urls))
#   prefix_default_language=True,
# )


urlpatterns += [
  path('ckeditor/',        include('ckeditor_uploader.urls')),
  path('tinymce/',         include('tinymce.urls')),
  path('i18n/',            include('django.conf.urls.i18n')),
  path('rosetta/',         include('rosetta.urls')),
  path('admin/',           custom_admin.urls),
  path('filebrowser/',     site.urls),
  path('sitemap.xml/',     sitemap, {'sitemaps':sitemaps}),
  path('robots.txt/',      robots, name='robots'),
  path('set_lang/<lang>/', set_lang,         name="set_lang"),
  path('jsi18n/',          js_cat.as_view(), name='javascript-catalog'),
  path('help/',            help, name='help'),


  path('',                 include('shop.item.api.urls')),
  path('',                 include('shop.cart.api.urls')),
  path('',                 include('shop.profile.urls')),

  path('',                 include('blog.api.urls')),
  
  path('',                 include('custom_auth.api.urls')),
]

from django.conf import settings

if settings.DEBUG == True:
  from django.conf.urls.static import static
  urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



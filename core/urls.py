from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import JavaScriptCatalog as js_cat

from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView as t_v


from django.contrib import admin
from core.admin import custom_admin
from core.views import *
from core.utils import *

from shop.item.sitemaps import *
from blog.post.sitemaps import *
from project.sitemaps import *

from filebrowser.sites import site


sitemaps = {
  'items': ItemSitemap,
  'categories': CategorySitemap,
  'posts': PostSitemap, 
  'static':StaticSitemap,
}

urlpatterns = []

urlpatterns += [
  path('ckeditor/',        include('ckeditor_uploader.urls')),
  path('tinymce/',         include('tinymce.urls')),
  path('rosetta/',         include('rosetta.urls')),
  path('i18n/',            include('django.conf.urls.i18n')),
  path('set_lang/<lang>/', set_lang,         name="set_lang"),
  path('sitemap.xml/',     sitemap, {'sitemaps':sitemaps}),
  path('robots.txt/',      robots, name='robots'),
  path('filebrowser/',     site.urls),
  path('jsi18n/',          js_cat.as_view(), name='javascript-catalog'),
  path('admin/',           custom_admin.urls),
  path('help/',            help, name='help'),

  path('', include('shop.item.api.urls')),
  path('', include('shop.cart.api.urls')),
  path('', include('shop.profile.api.urls')),
  
  path('', include('blog.post.api.urls')),
  path('', include('custom_auth.api.urls')),

  path('', include('starway.api.urls')),
  
]
multilingual_urls = [
  path('accounts/', include('allauth.urls')),
  path('test/', include('shop.test_shop.urls')),
  path('', include('shop.order.urls')),
  path('', include('shop.liqpay.urls')),
  path('', include('custom_admin.urls')),
  path('', include('page.urls')),
  
  path('starway/', include('starway.urls')),
  path('helper/', include('helper.urls')),
  path('chat/', include('chat.urls')),
]


if settings.MULTILINGUAL:
  urlpatterns += i18n_patterns(
    path('', include(multilingual_urls)),
    prefix_default_language=True,
  )
else:
  urlpatterns += [
    path('', include(multilingual_urls))
  ]



if settings.DEBUG == True:
  urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'core.views.handler_404'
handler500 = 'core.views.handler_500'

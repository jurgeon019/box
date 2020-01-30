from filebrowser.sites import site
from box.views import robots
from box.utils import set_lang
from box.admin import custom_admin, admin_plus
from django.contrib import admin
from django.urls import path, include 
from django.views.i18n import JavaScriptCatalog as js_cat
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView as t_v

from box.shop.item.sitemaps import *
from box.blog.sitemaps import *
from project.sitemaps import *


admin.site.site_header = "STARWAY CMS"
admin.site.site_title = "STARWAY CMS"
admin.site.index_title = "STARWAY CMS"


sitemaps = {
  'items': ItemSitemap,
  'categories': CategorySitemap,
  'posts': PostViewSitemap, 
  'static':StaticViewSitemap,
}


handler404 = 'box.views.handler_404'
handler500 = 'box.views.handler_500'


urlpatterns = [
  
  path('i18n/',            include('django.conf.urls.i18n')),
  path('rosetta/',         include('rosetta.urls')),
  # path('admin+/',          admin_plus.urls),
  # path('admin/',           custom_admin.urls),
  path('admin/',           admin.site.urls),
  path('tinymce/',         include('tinymce.urls')),
  path('filebrowser/',     site.urls),
  path('ckeditor/',        include('ckeditor_uploader.urls')),
  path('sitemap.xml/',     sitemap, {'sitemaps':sitemaps}),
  path('robots.txt/',      robots, name='robots'),
  path('set_lang/<lang>/', set_lang,         name="set_lang"),
  path('jsi18n/',          js_cat.as_view(), name='javascript-catalog'),
  path('help/',            help, name='help'),

  path('test/', include('box.shop.test_shop.urls')),
  
  path('',  include('box.shop.profile.api.urls')),
  path('',  include('box.shop.cart.api.urls')),
  path('',  include('box.shop.item.api.urls')),
  path('',  include('box.shop.liqpay.api.urls')),
  path('',  include('box.shop.order.api.urls')),
  path('',  include('box.blog.api.urls')),
  path('',  include('box.custom_auth.api.urls')),
]

from django.conf import settings

if settings.DEBUG == True:
  from django.conf.urls.static import static
  urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)







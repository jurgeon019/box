from django.contrib import admin
from django.urls import path, include 
from django.views.i18n import JavaScriptCatalog as js_cat
from django.contrib.sitemaps.views import sitemap
from django.conf import settings

from filebrowser.sites import site

from box.core.views import robots, set_lang, testmail
from box.core.admin import custom_admin, admin_plus
from box.shop.item.sitemaps import ItemSitemap, CategorySitemap
from box.blog.sitemaps import PostSitemap
from project.sitemaps import StaticSitemap


admin.site.site_header = "STARWAY CMS"
admin.site.site_title = "STARWAY CMS"
admin.site.index_title = "STARWAY CMS"


sitemaps = {
  'items':      ItemSitemap,
  'categories': CategorySitemap,
  'posts':      PostSitemap, 
  'static':     StaticSitemap,
}


handler404 = 'box.core.views.handler_404'
handler500 = 'box.core.views.handler_500'



api_urls = [
  path('', include('box.shop.novaposhta.api.urls')),
  path('', include('box.shop.customer.api.urls')),
  path('', include('box.shop.cart.api.urls')),
  path('', include('box.shop.item.api.urls')),
  path('', include('box.shop.liqpay.api.urls')),
  path('', include('box.shop.order.api.urls')),
  path('', include('box.blog.api.urls')),
  path('', include('box.custom_auth.api.urls')),
  path('', include('box.custom_admin.api.urls')),
  path('', include('box.contact_form.api.urls')),
]

urlpatterns = [
  path('admin_tools/',     include('admin_tools.urls')),
  # path('selectable/',      include('selectable.urls')),
  path('grappelli/',       include('grappelli.urls')),
  path('i18n/',            include('django.conf.urls.i18n')),
  path('rosetta/',         include('rosetta.urls')),
  path('admin+/',          admin_plus.urls),
  path('admin/',           admin.site.urls),
  path('tinymce/',         include('tinymce.urls')),
  path('filebrowser/',     site.urls),
  path('ckeditor/',        include('ckeditor_uploader.urls')),
  path('sitemap.xml/',     sitemap, {'sitemaps':sitemaps}),
  path('robots.txt/',      robots, name='robots'),
  path('set_lang/<lang>/', set_lang,         name="set_lang"),
  path('jsi18n/',          js_cat.as_view(), name='javascript-catalog'),
  path('testmail/',        testmail, name='testmail'),

  path('test/',          include('box.shop.test_shop.urls')),
  path('', include('box.global_config.urls')),
  path('', include('box.shop.novaposhta.urls')),

  # path('api/', include(api_urls))
  path('', include(api_urls))

]


if settings.DEBUG == True:
  from django.conf.urls.static import static
  urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)







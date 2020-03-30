from django.contrib import admin
from django.urls import path, include 
from django.views.i18n import JavaScriptCatalog as js_cat
from django.contrib.sitemaps.views import sitemap
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings

from filebrowser.sites import site

from box.core.views import robots, set_lang, testmail
from box.core.admin import admin_plus
from box.shop.item.sitemaps import ItemSitemap, ItemCategorySitemap
from box.blog.sitemaps import PostSitemap, PostCategorySitemap
from box.core.sitemaps import StaticSitemap


admin.site.site_header = "STARWAY CMS"
admin.site.site_title = "STARWAY CMS"
admin.site.index_title = "STARWAY CMS"

sitemaps = {
  'items':           ItemSitemap,
  'item_categories': ItemCategorySitemap,
  'posts':           PostSitemap, 
  'post_categories': PostCategorySitemap, 
  'static':          StaticSitemap,
}

handler404 = 'box.core.views.handler_404'
handler500 = 'box.core.views.handler_500'

multilingual_urls = [
  path('accounts/', include('allauth.urls')),
  path('rosetta/',         include('rosetta.urls')),
  path('admin+/',          admin_plus.urls),
  path('admin/',           admin.site.urls),
  path('', include('box.content.urls')),
  path('', include('box.shop.item.admin.urls')),
]
for url in settings.PROJECT_CORE_MULTILINGUAL_URLS:
  multilingual_urls.append(path('', include(url)))

api_urls = [
  path('', include('box.shop.customer.api.urls')),
  path('', include('box.shop.cart.api.urls')),
  path('', include('box.shop.item.api.urls')),
  path('', include('box.shop.order.api.urls')),
  path('', include('box.blog.api.urls')),
  path('', include('box.custom_auth.api.urls')),
  path('', include('box.custom_admin.api.urls')),
  path('', include('box.contact_form.api.urls')),
  path('', include('box.novaposhta.api.urls')),
  path('', include('box.content.api.urls')),
  path('', include('box.payment.liqpay.api.urls')),
]

third_party_urlpatterns = [
  path('admin_tools/',     include('admin_tools.urls')),
  path('grappelli/',       include('grappelli.urls')),
  path('i18n/',            include('django.conf.urls.i18n')),
  # path('rosetta/',         include('rosetta.urls')),
  # path('admin+/',          admin_plus.urls),
  # path('admin/',           admin.site.urls),
  path('tinymce/',         include('tinymce.urls')),
  path('filebrowser/',     site.urls),
  path('ckeditor/',        include('ckeditor_uploader.urls')),
  path('sitemap.xml/',     sitemap, {'sitemaps':sitemaps}),
  path('robots.txt/',      robots,           name='robots'),
  path('set_lang/<lang>/', set_lang,         name="set_lang"),
  path('jsi18n/',          js_cat.as_view(), name='javascript-catalog'),
]

box_urlpatterns = [
  path('testmail/',        testmail, name='testmail'),
  path('test/',          include('box.shop.test_shop.urls')),
  path('', include('box.global_config.urls')),
  path('', include('box.novaposhta.urls')),
  path('', include(api_urls)),
  path('api/', include(api_urls)),
]

urlpatterns = [
  path('', include(third_party_urlpatterns)),
  path('', include(box_urlpatterns)),
  path('', include(third_party_urlpatterns)),
]
for url in settings.PROJECT_CORE_URLS:
  urlpatterns.append(path('', include(url)))

urlpatterns += i18n_patterns(
  path('', include(multilingual_urls)),
  prefix_default_language=True,
)

if settings.DEBUG == True:
  urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include 
from django.views.i18n import JavaScriptCatalog as js_cat
from django.contrib.sitemaps.views import sitemap
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.views.decorators.cache import cache_page

from . import settings as core_settings
from filebrowser.sites import site
from box.core.views import robots, set_lang, testmail
from box.core.sitemaps import StaticSitemap

from importlib import import_module

sitemaps = {
    'static':  StaticSitemap,
}
for project_name, path_name in settings.SITEMAP_PATHS.items():
  try:
    p, m      = path_name.rsplit('.', 1)
    mod       = import_module(p)
    met       = getattr(mod, m)
    print(met)
    # path_name = import_module(path_name)
    sitemaps.update({
      project_name:met
    })
  except:
    pass
if 'box.core.sw_content' in settings.INSTALLED_APPS:
  from box.core.sw_content.sitemaps import PageSitemap
  sitemaps.update({
    'pages':PageSitemap,
  })
if 'box.apps.sw_shop.sw_catalog' in settings.INSTALLED_APPS:
  from box.apps.sw_shop.sw_catalog.sitemaps import ItemSitemap, ItemCategorySitemap
  sitemaps.update({
  'items':           ItemSitemap,
  'item_categories': ItemCategorySitemap,
  })
if 'box.apps.sw_blog' in settings.INSTALLED_APPS:
  from box.apps.sw_blog.sitemaps import PostSitemap, PostCategorySitemap
  sitemaps.update({
    'posts':           PostSitemap, 
    'post_categories': PostCategorySitemap, 
  })

static_urlpatterns = []

if settings.DEBUG == True:
  static_urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
  static_urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "STARWAY CMS"
admin.site.site_title  = "STARWAY CMS"
admin.site.index_title = "STARWAY CMS"

handler404 = 'box.core.views.handler_404'
handler500 = 'box.core.views.handler_500'

PROJECT_CORE              = [path('', include(url)) for url in core_settings.PROJECT_CORE_URLS]
PROJECT_CORE_MULTILINGUAL = [path('', include(url)) for url in core_settings.PROJECT_CORE_MULTILINGUAL_URLS]

excluded_apps = [
  'box.core', 
  'box.apps.sw_shop', 
  'box.apps.sw_payment',
  'box.apps.sw_delivery',
]
box_apps          = [app for app in settings.INSTALLED_APPS if app.startswith('box.') and  app not in excluded_apps]  #https://stackoverflow.com/questions/4843158/check-if-a-python-list-item-contains-a-string-inside-another-string
box               = [path('', include(f'{app}.urls')) for app in box_apps]
box_multilingual  = [path('', include(f'{app}.multilingual_urls')) for app in box_apps]

multilingual = i18n_patterns(
  path('admin/',    admin.site.urls),
  path('accounts/', include('allauth.urls')),
  path('rosetta/',  include('rosetta.urls')),
  *box_multilingual,
  *PROJECT_CORE_MULTILINGUAL,
  prefix_default_language=core_settings.PREFIX_DEFAULT_LANGUAGE,
)

urlpatterns = [
  *static_urlpatterns,
  path('sitemap.xml/',     sitemap, {'sitemaps':sitemaps}, name='sitemap'),
  path('robots.txt/',      robots,           name='robots'),
  # path('sitemap.xml/',     cache_page(60)(sitemap), {'sitemaps': sitemaps}, name='cached-sitemap'),
  # path('robots.txt/',      include('robots.urls')),
  path('i18n/',            include('django.conf.urls.i18n')),
  path('set_lang/<lang>/', set_lang,         name="set_lang"),
  path('jsi18n/',          js_cat.as_view(), name='javascript-catalog'),
  path('admin_tools/',     include('admin_tools.urls')),
  path('grappelli/',       include('grappelli.urls')),
  path('tinymce/',         include('tinymce.urls')),
  path('ckeditor/',        include('ckeditor_uploader.urls')),
  path('api-auth/',        include('rest_framework.urls', namespace='rest_framework')),
  path('auth/',            include('djoser.urls')),
  path('auth/',            include('djoser.urls.authtoken')),
  path('auth/',            include('djoser.urls.jwt')),
  path('_nested_admin/',   include('nested_admin.urls')),
  path('filebrowser/',     site.urls),
  *box,
  *PROJECT_CORE,
  *multilingual,
]

# if settings.DEBUG:
if core_settings.DJANGO_DEBUG_TOOLBAR_ON:
    print('sdfsdf')
    import debug_toolbar
    urlpatterns.extend([
        path('__debug__/', include(debug_toolbar.urls)),
    ])





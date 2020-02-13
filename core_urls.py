from django.urls import path, include




urlpatterns = [
  path('', include('box.urls')),
]

multilingual_urls = [
  path('', include('box.multilingual_urls')),
  path('', include('project.urls')),
]

from django.conf import settings 
from django.conf.urls.i18n import i18n_patterns

if not settings.USE_I18N:
  urlpatterns += [
    path('', include(multilingual_urls)),
  ]
else:
  urlpatterns += i18n_patterns(
    path('', include(multilingual_urls)),
    prefix_default_language=False,
  )



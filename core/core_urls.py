from box.core.urls import * 

from django.conf import settings 
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from importlib import import_module



def get_urlpatterns():
  urlpatterns = [
    path('', include('box.core.urls')),
  ]
  try:
    urlconf_module = import_module('project.api.urls')
    urlpatterns += ['project.api.urls']
  except:
    pass
  return urlpatterns

urlpatterns = get_urlpatterns()

multilingual_urls = [
  path('', include('box.core.multilingual_urls')),
  path('', include('project.urls')),
]


urlpatterns += i18n_patterns(
  path('', include(multilingual_urls)),
  prefix_default_language=True,
)





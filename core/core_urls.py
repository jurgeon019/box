from django.conf import settings 
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include


multilingual_urlpatterns = [
  path('accounts/', include('allauth.urls')),
  path('', include('box.page.urls')),
  path('', include('box.shop.item.urls')),
]




urlpatterns = [
  path('', include('box.core.urls')),
  # path('', include('project.api.urls'))
]
multilingual_urls = [
  # path('', include('box.core.multilingual_urls')),
  path('', include(multilingual_urlpatterns)),
  path('', include('project.urls')),
]

urlpatterns += i18n_patterns(
  path('', include(multilingual_urls)),
  prefix_default_language=True,
)





from django.conf import settings 


def get(x, y): return getattr(settings, x, y)


IMAGE_NOT_FOUND                = get(
    'IMAGE_NOT_FOUND', '/static/core/img/photo_not_found.jpg')
SHOW_ADMIN                     = get(
    'SHOW_ADMIN', False)
PREFIX_DEFAULT_LANGUAGE        = get(
    'PREFIX_DEFAULT_LANGUAGE', True)
STATIC_SITEMAP_PAGES           = get(
    'STATIC_SITEMAP_PAGES', [])
PROJECT_CORE_MULTILINGUAL_URLS = get(
    'PROJECT_CORE_MULTILINGUAL_URLS', [])
PROJECT_CORE_URLS              = get(
    'PROJECT_CORE_URLS', [])

DEFAULT_RECIPIENT_LIST = [
    'jurgeon018@gmail.com',
]
DJANGO_DEBUG_TOOLBAR_ON = get(
    'DJANGO_DEBUG_TOOLBAR_ON', False)

CAPTCHA_V2_PUBLIC = 'SDF'
CAPTCHA_V2_SECRET = 'SDF'
CAPTCHA_V3_PUBLIC = 'SDF'
CAPTCHA_V3_SECRET = 'SDF'




from django.conf import settings 


DEFAULT_FAVICON           = '/static/core/favicon/favicon.ico'
DEFAULT_OGIMAGE_SQUARE    = '/static/core/ogimages/ogimage.png'
DEFAULT_OGIMAGE_RECTANGLE = '/static/core/ogimages/ogimage.png'
DEFAULT_IMAGE_NOT_FOUND   = '/static/core/img/photo_not_found.jpg'
DEFAULT_SHOW_ADMIN        = False 
FAVICON              = getattr(settings, 'FAVICON', DEFAULT_FAVICON)
OGIMAGE_SQUARE       = getattr(settings, 'OGIMAGE_SQUARE', DEFAULT_OGIMAGE_SQUARE)
OGIMAGE_RECTANGLE    = getattr(settings, 'OGIMAGE_RECTANGLE', DEFAULT_OGIMAGE_RECTANGLE)
IMAGE_NOT_FOUND      = getattr(settings, 'IMAGE_NOT_FOUND', DEFAULT_IMAGE_NOT_FOUND)
SHOW_ADMIN           = getattr(settings, 'SHOW_ADMIN', DEFAULT_SHOW_ADMIN)


DEFAULT_PREFIX_DEFAULT_LANGUAGE = True
PREFIX_DEFAULT_LANGUAGE = getattr(
    settings, 'PREFIX_DEFAULT_LANGUAGE', DEFAULT_PREFIX_DEFAULT_LANGUAGE)


DEFAULT_STATIC_SITEMAP_PAGES = []
STATIC_SITEMAP_PAGES = getattr(
    settings, 'STATIC_SITEMAP_PAGES', DEFAULT_STATIC_SITEMAP_PAGES)


DEFAULT_PROJECT_CORE_MULTILINGUAL_URLS = []
PROJECT_CORE_MULTILINGUAL_URLS = getattr(
    settings, 'PROJECT_CORE_MULTILINGUAL_URLS', DEFAULT_PROJECT_CORE_MULTILINGUAL_URLS)

DEFAULT_PROJECT_CORE_URLS = []
PROJECT_CORE_URLS = getattr(
    settings, 'PROJECT_CORE_URLS', DEFAULT_PROJECT_CORE_URLS)




DEFAULT_RECIPIENT_LIST = [
    'jurgeon018@gmail.com',
]


CAPTCHA_V2_PUBLIC = 'SDF'
CAPTCHA_V2_SECRET = 'SDF'
CAPTCHA_V3_PUBLIC = 'SDF'
CAPTCHA_V3_SECRET = 'SDF'


DEFAULT_DJANGO_DEBUG_TOOLBAR_ON = False  
DJANGO_DEBUG_TOOLBAR_ON = getattr(settings, 'DJANGO_DEBUG_TOOLBAR_ON', DEFAULT_DJANGO_DEBUG_TOOLBAR_ON)
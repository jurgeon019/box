from django.conf import settings 


DEFAULT_FAVICON           = '/static/core/favicon/favicon.ico'
DEFAULT_OGIMAGE_SQUARE    = '/static/core/ogimages/ogimage.png'
DEFAULT_OGIMAGE_RECTANGLE = '/static/core/ogimages/ogimage.png'
DEFAULT_IMAGE_NOT_FOUND   = '/static/core/img/photo_not_found.jpg'
DEFAULT_SHOW_ADMIN        = False 

FAVICON            = getattr(settings, 'FAVICON', DEFAULT_FAVICON)
OGIMAGE_SQUARE     = getattr(settings, 'OGIMAGE_SQUARE', DEFAULT_OGIMAGE_SQUARE)
OGIMAGE_RECTANGLE  = getattr(settings, 'OGIMAGE_RECTANGLE', DEFAULT_OGIMAGE_RECTANGLE)
IMAGE_NOT_FOUND    = getattr(settings, 'IMAGE_NOT_FOUND', DEFAULT_IMAGE_NOT_FOUND)
SHOW_ADMIN         = getattr(settings, 'SHOW_ADMIN', DEFAULT_SHOW_ADMIN)


DEFAULT_RECIPIENT_LIST = [
    'jurgeon018@gmail.com',
]


CAPTCHA_V2_PUBLIC = 'SDF'
CAPTCHA_V2_SECRET = 'SDF'
CAPTCHA_V3_PUBLIC = 'SDF'
CAPTCHA_V3_SECRET = 'SDF'



import os 
from .default import BASE_DIR
from django.utils.translation import gettext_lazy as _

TIME_ZONE = 'UTC' #'Europe/Kiev'
USE_I18N = True
USE_L10N = True 
USE_TZ = True

LANGUAGES = [
    ('uk', _('Українська')),
    ('en', _('Англійська')),
    ('ru', _('Російська')),
    # ('en-us', ('en')),
]
LANGUAGE_CODE = 'uk' 
LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),)
MODELTRANSLATION_DEFAULT_LANGUAGE = 'uk'
ROSETTA_MESSAGES_PER_PAGE = 300



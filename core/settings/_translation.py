import os 
from ._django import BASE_DIR
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
MODELTRANSLATION_DEFAULT_LANGUAGE = LANGUAGE_CODE
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
ROSETTA_MESSAGES_PER_PAGE = 100



import os 
from ._django import BASE_DIR
from django.utils.translation import gettext_lazy as _
TIME_ZONE = 'UTC' #'Europe/Kiev'
USE_I18N = True
# USE_L10N = False  
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
ROSETTA_ENABLE_TRANSLATION_SUGGESTIONS = True
# YANDEX_TRANSLATE_KEY = 'trnsl.1.1.20200327T033955Z.7e48435c2547f277.fffb24ccd1d9ddde9374eb10b4d05a2157ef725c'
AZURE_CLIENT_SECRET = "fa4b9549dca24df88eeb6c58ada57bed"

DATE_FORMAT = "d-m-Y H:M"


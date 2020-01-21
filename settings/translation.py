import os 
from .default import BASE_DIR

TIME_ZONE = 'UTC' #'Europe/Kiev'
USE_L10N = True
USE_I18N = True
USE_TZ = True
LANGUAGES = (
  ('ru', ('ru')),
  ('en', ('en')),
  ('uk', ('uk')),
)
LANGUAGE_CODE = 'uk'
LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),)
MODELTRANSLATION_DEFAULT_LANGUAGE = 'uk'
ROSETTA_MESSAGES_PER_PAGE = 100



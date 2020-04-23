from django.conf import settings 

def get(a, b):
    return getattr(settings, a, b) 

MULTIPLE_CATEGORY      = get('MULTIPLE_CATEGORY', False) 
ITEM_SEARCH_FIELDS     = get('ITEM_SEARCH_FIELDS', ['code',]) 
ITEM_URL_NAME          = get('ITEM_URL_NAME', "item")
ITEM_MEDIA_PATH        = get('ITEM_MEDIA_PATH',  '/')
ITEM_CATEGORY_URL_NAME = get('ITEM_CATEGORY_URL_NAME', 'item_category')

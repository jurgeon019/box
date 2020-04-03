from django.conf import settings 


DEFAULT_MULTIPLE_CATEGORY = False
DEFAULT_ITEM_SEARCH_FIELDS = [
    'code',
]



MULTIPLE_CATEGORY  = getattr(settings, 'MULTIPLE_CATEGORY', DEFAULT_MULTIPLE_CATEGORY) 
ITEM_SEARCH_FIELDS = getattr(settings, 'ITEM_SEARCH_FIELDS', DEFAULT_ITEM_SEARCH_FIELDS) 




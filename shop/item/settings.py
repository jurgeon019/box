from django.conf import settings


PAGINATE_AJAX = getattr(settings, 'PAGINATE_AJAX', True)
SEARCH_FIELDS = getattr(settings, 'SEARCH_FIELDS', ['code', ])
NO_ITEM_IMAGE = getattr(settings, 'NO_ITEM_IMAGE', '/static/dist/img/photo_not_found.jpg')






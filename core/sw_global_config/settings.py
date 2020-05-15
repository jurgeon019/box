from django.conf import settings 

def get(x, y): return getattr(settings, x, y)


META_ROBOTS       = get('META_ROBOTS', None)#"noindex, nofollow")
FAVICON           = get('FAVICON', 'favicon/favicon.ico')
OGIMAGE_SQUARE    = get('OGIMAGE_SQUARE', 'ogimage/square.png')
OGIMAGE_RECTANGLE = get('OGIMAGE_RECTANGLE', 'ogimage/rectangle.png')








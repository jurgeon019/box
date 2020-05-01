from django.conf import settings 

def get(x, y):
    return getattr(settings, x, y)


FAVICON    = get('FAVICON', 'favicon/favicon.ico')
OGIMAGE_SQUARE                 = get(
    'OGIMAGE_SQUARE', 'ogimage/square.png')
OGIMAGE_RECTANGLE              = get(
    'OGIMAGE_RECTANGLE', 'ogimage/rectangle.png')
RECIPIENTS = get('RECIPIENTS', ['jurgeon018@gmail.com',])


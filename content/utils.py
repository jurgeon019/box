from box.content.models import *


def set_page(obj, page_code=None):
    if page_code:
        page = Page.objects.filter(code=page_code)
        if page.exists:
            obj.page = page.first() 
            obj.save()


def get_class(content_type):
    mapper = {
        'map':     Map,
        'img':     Img,
        'tiny':    Text,
        'plain':   Text,
        'address': Address,
        'tel':     Tel,
        'mailto':  Mailto,
        'link':    Link,
        'slider':  Slider,
        'slide':   Slide,
        'item':          Item,
        'item_category': ItemCategory,
        'post':          Post,
        'post_category': PostCategory,
    }
    return mapper[content_type] 




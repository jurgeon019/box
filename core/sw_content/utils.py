from box.core.sw_content.models import *
from django.conf import settings 



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
    }
    if 'box.sw_shop.item' in settings.INSTALLED_APPS:
        from box.sw_shop.item.models import Item, ItemCategory
        mapper.update({
            'item':          Item,
            'item_category': ItemCategory,
        })
    if 'box.sw_blog' in settings.INSTALLED_APPS:
        from box.sw_blog.models import Post, PostCategory
        mapper.update({
            'post':          Post,
            'post_category': PostCategory,
        })
    return mapper[content_type] 




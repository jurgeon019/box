from box.page.models import Img, Text, Page
from box.shop.item.models import Item, ItemCategory
from box.blog.models import Post, PostCategory
from box.slider.models import Slide, Slider


def set_page(obj, page_code=None):
    if page_code:
        page = Page.objects.filter(code=page_code)
        if page.exists:
            obj.page = page.first() 
            obj.save()

def get_class(content_type):
    mapper = {
        'plain':Text,
        'tiny':Text,
        'image':Img,
        'slider':Slider,
    }
    klass = mapper[content_type]
    return klass 




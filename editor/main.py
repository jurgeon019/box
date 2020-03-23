from django.utils.html import mark_safe, strip_tags
from django.shortcuts import reverse, render
from django.template.loader import render_to_string

from box.slider.models import Slide
from .utils import get_class, set_page


def render_post(code):
    pass 

def render_post_category(code):
    pass 

def render_item(code):
    pass 

def render_item_category(code):
    pass 


def render_content(code, content_type, page_code=None):
    klass    = get_class(content_type)
    obj      = klass.objects.get_or_create(code=code)[0]
    if content_type == 'slider':
        obj = Slide.objects.filter(slider=obj).all()
    result   = {
        # 'content':mark_safe(content),
        'obj':obj,
    }
    set_page(obj=obj, page_code=page_code)
    return result








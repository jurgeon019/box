from django.utils.html import mark_safe, strip_tags
from django.shortcuts import reverse, render
from django.template.loader import render_to_string

from box.core.sw_content.models import Slide
from .utils import get_class, set_page


def get_context(content_type, code, page_code=None):
    obj = get_class(content_type).objects.get_or_create(code=code)[0]
    if content_type == 'slider':
        obj = Slide.objects.all().filter(slider=obj)
    set_page(obj=obj, page_code=page_code)
    context = {
        'obj':obj,
    }
    return context 


def render_post(code):
    pass 

def render_post_category(code):
    pass 

def render_item(code):
    pass 

def render_item_category(code):
    pass 





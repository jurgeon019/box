from django import template
from django.utils.html import mark_safe, strip_tags
from django.shortcuts import reverse 


import sys 

from ..models import *


register = template.Library()

def render(feature_code, page_code, type):
    feature, _ = PageFeature.objects.get_or_create(code=feature_code)
    if page_code:
        # page, _ = Page.objects.get_or_create(code=page_code)
        page = Page.objects.filter(code=page_code)
        if page.exists:
            page = page.first()
            feature.page = page 
            feature.save()
    result = ''
    model = ''
    id = ''
    admin_url = ''
    field = ''
    if feature.value:
        result = feature.value
        if type == 'plain':
            result = strip_tags(result)
        model = feature._meta.model_name
        app_label = feature._meta.app_label
        id    = feature.id
        field = 'value'
        admin_url = reverse(f'admin:{app_label}_{model}_change', args=(feature.pk,))
    result = mark_safe(f'<div class="db_content" data-admin_url="{admin_url}" data-class="{model}" data-field="{field}" data-id="{id}">{result}</div>')
    return result

@register.simple_tag
def plain(feature_code, page_code=None):
    result = render(feature_code, page_code, type='plain')
    return result 



@register.simple_tag
def tiny(feature_code, page_code=None):
    result = render(feature_code, page_code, type='tiny')
    return result 








@register.simple_tag
def get_feature(page_code, page_feature_code):
    page    = Page.objects.get(code=page_code)
    print(page)
    feature = page.features.get(code=page_feature_code)
    return feature


@register.simple_tag
def get_features_by_attr(page_code, attr):
    page    = Page.objects.get(code=page_code)
    # sliders = page.sliders.all()
    sliders = getattr(page, attr).all()
    return sliders


@register.simple_tag
def get_features_by_class(page_code, classname):
    page    = Page.objects.get(code=page_code)
    # sliders = Slider.objects.filter(page__code=page_code)
    sliders = getattr(sys.modules[__name__], classname).objects.filter(page__code=page_code)
    return sliders




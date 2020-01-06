import sys 
from django import template
from pages.models import *
register = template.Library()



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




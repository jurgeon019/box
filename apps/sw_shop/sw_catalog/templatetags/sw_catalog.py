from django import template
from ..models import *


register = template.Library()


@register.filter
def get_type(value):
    return type(value)


@register.simple_tag
def get_item_attribute_values(item, code):
    return item.get_item_attribute_values(code)




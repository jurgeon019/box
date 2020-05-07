from django import template
from box.apps.sw_shop.sw_cart.utils import get_cart
from box.apps.sw_shop.sw_cart.models import CartItemAttribute
from box.apps.sw_shop.sw_catalog.models import (
    ItemAttributeValue, ItemAttribute, Attribute,
)


register = template.Library()


# @register.filter
@register.simple_tag
def get_cart_item_attribute(cart_item, attr_code):
    try:
        attr = CartItemAttribute.objects.get(
            cart_item=cart_item,
            attribute_name=ItemAttribute.objects.get(item=cart_item.item,attribute__code=attr_code),
            # attribute_name=Attribute.objects.get(code=attr_code),
        ) 
    except:
        attr = None 
    return attr



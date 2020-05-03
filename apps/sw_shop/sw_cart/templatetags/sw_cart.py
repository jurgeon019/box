from django import template
from box.apps.sw_shop.sw_cart.utils import get_cart
from box.apps.sw_shop.sw_cart.models import CartItemAttribute
from box.apps.sw_shop.sw_catalog.models import (
    ItemAttributeVariant, ItemAttribute, Attribute,
)


register = template.Library()


# @register.filter
@register.simple_tag
def get_cart_item_attribute(cart_item, attr_code):
    print(cart_item)
    print(attr_code)
    attr = Attribute.objects.get(code=attr_code)
    attr = CartItemAttribute.objects.get(
        cart_item=cart_item,
        # attribute_name__code=attr_code
        attribute_name=attr,
    ) 
    return attr#.value.code



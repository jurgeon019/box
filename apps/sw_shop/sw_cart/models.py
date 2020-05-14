from django.db import models 
from django.contrib.auth import get_user_model 
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.db.models import Sum

from box.apps.sw_shop.sw_catalog.models import (
  Item, Currency, Attribute, AttributeValue, ItemAttribute, ItemAttributeValue
)


class Cart(models.Model):
  user    = models.ForeignKey(
    verbose_name=_("Користувач"), to=get_user_model() , on_delete=models.SET_NULL, 
    related_name='carts', blank=True, null=True,
  )
  order   = models.OneToOneField(
    verbose_name=_("Замовлення"), to="sw_order.Order", blank=True, null=True, 
    on_delete=models.CASCADE, related_name='cart',
  )
  ordered = models.BooleanField(
    verbose_name=_("Замовлено"), default=False,
  )
  created = models.DateTimeField(
    verbose_name=_('Дата створення'), default=timezone.now,
  )
  updated = models.DateTimeField(
    verbose_name=_('Дата оновлення'),  auto_now_add=False, auto_now=True,  
    blank=True, null=True,
  )

  def __str__(self):
    return f"{self.id}"

  class Meta:
    verbose_name = _('Корзина')
    verbose_name_plural = _('Корзини')

  def get_cart_item_with_attributes(self, item, attributes):
    cart_item = CartItem.objects.filter(item=item, cart=self)
    for attribute in attributes:
      CartItemAttribute.objects.filter(
        cart_item=cart_item,
        attribute_name__id=attribute['item_attribute_id'],
        value__id=attribute['item_attribute_value_id'],
      )
    # TODO:???
    return cart_item

  def get_cart_item_attributes(self, item, attribute):
    # if attribute:
    print("attribute:", attribute)
    cart_item_attributes = CartItemAttribute.objects.filter(
      cart_item__item=item,
      attribute_name=ItemAttribute.objects.get(id=attribute['item_attribute_id']),
      value=ItemAttributeValue.objects.get(id=attribute['item_attribute_value_id']),
    )
    return cart_item_attributes

  def create_cart_item_attributes(self, cart_item, attributes):
    CartItemAttribute.objects.filter(cart_item=cart_item).delete()
    for attribute in attributes:
      # if 'item_attribute_id' in attribute.keys() and 'item_attribute_value_id' in attribute.keys():
      if attribute:
        attribute_name  = ItemAttribute.objects.get(id=attribute['item_attribute_id'])
        attribute_value = ItemAttributeValue.objects.get(id=attribute['item_attribute_value_id'])
        print("attribute:", attribute)
        print("attribute_name:", attribute_name)
        print("attribute_value:", attribute_value)
        CartItemAttribute.objects.create(
          cart_item=cart_item,
          attribute_name=attribute_name,
          value=attribute_value,
          price=attribute_value.price
        )

  def add_item(self, item_id, quantity, attributes=None):
    try: quantity = int(quantity)
    except: quantity = 1
    item = Item.objects.get(pk=int(item_id))
    if attributes:
      print("attributes:", attributes)
      for attribute in attributes:
        cart_item_attributes = self.get_cart_item_attributes(item, attribute)
        # print("cart_item_attributes:",cart_item_attributes)
        # if cart_item_attributes and not cart_item_attributes.exists():
        if not cart_item_attributes.exists():
        # if True:
          cart_item = CartItem.objects.create(item=item, cart=self)
          cart_item.quantity=quantity
          cart_item.save()
          self.create_cart_item_attributes(cart_item, attributes)
          break 
        else:
          print('ELSE!')
          # cart_item = self.get_cart_item_with_attributes(item, attributes)
          # cart_item.quantity += int(quantity)
          # cart_item.save()
    else:
      cart_item, created = CartItem.objects.get_or_create(
        cart=self,
        item=item,
      )
      if created:
        cart_item.quantity = int(quantity)
      elif not created:
        cart_item.quantity += int(quantity)
      cart_item.save()
      
  def change_cart_item_amount(self, cart_item_id, quantity):
    try: quantity = int(quantity)
    except: quantity = 1
    cart_item = CartItem.objects.get(
      id=cart_item_id, 
      cart=self,
    )
    cart_item.quantity = quantity
    cart_item.save()
    return cart_item 
  
  def change_item_amount(self, item_id, quantity):
    try: quantity = int(quantity)
    except: quantity = 1
    cart_item = CartItem.objects.get(
      item__id=item_id,
      cart=self,
    )
    cart_item.quantity = quantity
    cart_item.save()
    return cart_item
  
  def remove_cart_item(self, cart_item_id):
    CartItem.objects.get(
      cart=self,
      id=cart_item_id,
    ).delete()

  def clear(self):
    CartItem.objects.filter(cart=self).delete()
    # self.items.all().delete()

  @property
  def items_quantity(self):
    items_quantity = 0
    # for cart_item in self.items.all():
    for cart_item in CartItem.objects.filter(cart=self):
      items_quantity += cart_item.quantity
    return items_quantity
  
  @property
  def items_count(self):
    items_count = CartItem.objects.filter(cart=self).all().count()
    items_count = self.items.all().count()
    return items_count

  @property
  def total_price(self):
    total_price = 0
    for cart_item in self.items.all():
    # for cart_item in CartItem.objects.filter(cart=self):
      if cart_item.total_price:
        total_price += cart_item.total_price
    print(total_price)
    return float(total_price)

  @property
  def currency(self):
    return Currency.objects.get(is_main=True).code


class CartItemAttribute(models.Model):
  cart_item = models.ForeignKey(
    verbose_name=_("Товар в корзині"), on_delete=models.CASCADE,
    to="sw_cart.CartItem", related_name='attributes',
  )
  attribute_name = models.ForeignKey(
    to="sw_catalog.ItemAttribute", on_delete=models.CASCADE,
    verbose_name=_("Атрибут"),
  )
  value = models.ForeignKey(
    to="sw_catalog.ItemAttributeValue", on_delete=models.CASCADE,
    verbose_name=_("Значення")
  )
  price = models.FloatField(
    # verbose_name=_("Ціна"), null=False, blank=False, default=0,
    verbose_name=_("Ціна"), null=True, blank=True, default=0,
  )

  class Meta: 
    verbose_name = _('вибраний атрибут у товара в корзині')
    verbose_name_plural = _('вибрані атрибути у товарів в корзині')
  
  def __str__(self):
    # return f'{self.cart_item.item.title}, {self.attribute_name.name}:{self.value.value}'
    return f'{self.cart_item.item.title}, {self.attribute_name.attribute.name}:{self.value.value.value}'


class CartItem(models.Model):
  ordered  = models.BooleanField(
     verbose_name=("Замовлено"), default=False,
    )
  cart     = models.ForeignKey(  
     to='sw_cart.Cart',   verbose_name=("Корзина"), on_delete=models.CASCADE, blank=True, null=True, related_name="items",
    )
  order    = models.ForeignKey(  
     to='sw_order.Order', verbose_name=('Замовлення'),   on_delete=models.CASCADE, blank=True, null=True, related_name="cart_items",
    )
  item     = models.ForeignKey(  
     to="sw_catalog.Item",   verbose_name=('Товар'),   
     on_delete=models.CASCADE, 
     blank=False, null=False, 
     related_name="cart_items",
    )
  quantity = models.IntegerField(
    verbose_name=_('Кількість'), default=1,
  )
  created  = models.DateTimeField(
    verbose_name=_('Дата создания'),  default=timezone.now
  )
  updated  = models.DateTimeField(
    verbose_name=_('Дата обновления'),auto_now_add=False, 
    auto_now=True,  blank=True, null=True
  )
  
  def get_attributes(self):
    return CartItemAttribute.objects.filter(cart_item=self)

  def get_attribute(self, attr_code):
    try:
        attr = CartItemAttribute.objects.get(
            cart_item=self,
            attribute_name=ItemAttribute.objects.get(item=self.item,attribute__code=attr_code),
            # attribute_name=Attribute.objects.get(code=attr_code),
        ) 
    except:
        attr = None 
    # print(attr)
    # print(attr.value.value.code)
    return attr 

  @property
  def total_price(self):
    total_price = self.price_per_item * self.quantity
    return total_price 

  @property
  def price_per_item(self):
    price_per_item = self.item.get_cart_price()
    attrs = self.get_attributes().aggregate(Sum('price'))['price__sum']
    if attrs:
      price_per_item += attrs
    return price_per_item 

  @property
  def currency(self):
    return self.cart.currency

  def __str__(self):
    return f'{self.item.title}, {self.quantity}, {self.total_price} {self.item.currency}'

  class Meta: 
    verbose_name = _('Товар в корзині')
    verbose_name_plural = _('Товари в корзині')


class FavourItem(models.Model):
  item = models.ForeignKey("sw_catalog.Item", on_delete=models.CASCADE, verbose_name='Улюблені товари', blank=True, null=True, related_name="favour_items")
  cart = models.ForeignKey('sw_cart.Cart', on_delete=models.CASCADE, verbose_name='Улюблені товари', blank=True, null=True, related_name="favour_items")
  
  def __str__(self):
    return f'{self.item.title}'

  class Meta:
    verbose_name=_("Улюблений товар")
    verbose_name_plural=_("Улюблені товари")





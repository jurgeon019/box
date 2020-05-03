from django.db import models 
from django.contrib.auth import get_user_model 
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from box.apps.sw_shop.sw_catalog.models import (
  Item, ItemCurrency, Attribute, AttributeVariantValue
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

  def create_cart_item_attributes(self, cart_item, attributes):
    CartItemAttribute.objects.filter(cart_item=cart_item).delete()
    for attribute in attributes:
      CartItemAttribute.objects.create(
        cart_item=cart_item,
        value=AttributeVariantValue.objects.get(id=attribute['value_id']),
        attribute_name=Attribute.objects.get(id=attribute['attribute_id']),
      )

  def get_cart_item_attributes(self, item, attribute):
      cart_item_attributes = CartItemAttribute.objects.filter(
        cart_item__item=item,
        attribute_name=Attribute.objects.get(id=attribute['attribute_id']),
        value=AttributeVariantValue.objects.get(id=attribute['value_id']),
      )
      return cart_item_attributes
    
  # def get_cart_item_with_attributes(self, item, attributes):
  #   cart_item = CartItem.objects.filter(item=item, cart=self)
  #   for attribute in attributes:
  # TODO:get_cart_item_with_attributes
  #   return cart_item


  def add_item(self, item_id, quantity, attributes=[]):
    """
    товар 1 з розміром 1 i кольором 1 додається в корзину 
    в корзині товар з розміром 1 і кольором 1 
    товар 1 з розміром 1 і кольором 2 додається в корзину 
    перевіряється чи немає товара в корзині з такими ж характеристиками
    якщо є то створюється новий товар 
    якщо нє то додається кількість 

    як перевірити шо в корзині є товар з такими ж характеристиками?
    """
    try: quantity = int(quantity)
    except: quantity = 1
    item = Item.objects.get(pk=int(item_id))

    # cart_item, created = CartItem.objects.get_or_create(
    #   cart=self,
    #   item=item,
    # )
    # if created:
    #   cart_item.quantity = int(quantity)
    # elif not created:
    #   cart_item.quantity += int(quantity)
    # cart_item.save()
    print(quantity)
    for attribute in attributes:
      cart_item_attributes = self.get_cart_item_attributes(item, attribute)
      if not cart_item_attributes.exists():
        cart_item = CartItem.objects.create(item=item, cart=self)
        cart_item.quantity=quantity
        cart_item.save()
        self.create_cart_item_attributes(cart_item, attributes)
        break 
      # else:
      #   # TODO: get_cart_item_with_attributes
      #   cart_item = get_cart_item_with_attributes(item=item)
      #   cart_item.quantity += int(quantity)
      #   cart_item.save()

      
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
    self.items.all().delete()

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

    #TODO: зробити сумування не пітонячим циклом, а якось пройтись SQLьом
    #TODO 2: не получиться, бо total_price зроблено через @property, а має бути окремим полем

    total_price = 0
    for cart_item in self.items.all():
    # for cart_item in CartItem.objects.filter(cart=self):
      if cart_item.total_price:
        total_price += cart_item.total_price
    return total_price

  @property
  def currency(self):
    currency = None 
    currencies = ItemCurrency.objects.filter(is_main=True)
    if currencies.exists():
      currency = currencies.first().code
    return currency


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
    #  blank=True, null=True, 
     related_name="cart_items",
    )
  quantity = models.IntegerField(
    verbose_name=_('Кількість'), default=1,
  )
  created  = models.DateTimeField(verbose_name=_('Дата создания'),  default=timezone.now)
  updated  = models.DateTimeField(verbose_name=_('Дата обновления'),auto_now_add=False, auto_now=True,  blank=True, null=True)

  # features = models.ManyToManyField(verbose_name=_("Атрибут"), "sw_sw_catalog.ItemAttribute")
  # options  = models.ManyToManyField(verbose_name=_("Атрибут"), "sw_catalog.ItemOption")
  
  @property
  def total_price(self):
    return self.item.price * self.quantity
    # if self.item and self.item.price
    # try:
    #   item = self.item.price
    #   if item:
    #     return item * self.quantity
    #   else:
    #     return None 
    # except:
    #   print('Блядь поправ це гімно, відвалюється при покупці в 1 клік')
    #   return 1

  @property
  def price_per_item(self):
    return self.item.price

  @property
  def currency(self):
    return self.cart.currency

  def __str__(self):
    return f'{self.item.title}, {self.quantity}, {self.total_price} {self.item.currency}'

  class Meta: 
    verbose_name = _('Товар в корзині')
    verbose_name_plural = _('Товари в корзині')



class CartItemAttribute(models.Model):
  cart_item = models.ForeignKey(
    verbose_name=_("Товар в корзині"), 
    to="sw_cart.CartItem",
    on_delete=models.CASCADE,
  )
  attribute_name = models.ForeignKey(
    to="sw_catalog.Attribute",
    on_delete=models.CASCADE,
    verbose_name=_("Атрибут"),
  )
  value = models.ForeignKey(
    to="sw_catalog.AttributeVariantValue",
    on_delete=models.CASCADE,
    verbose_name=_("Значення")
  )

  class Meta: 
    verbose_name = _('вибраний атрибут у товара в корзині')
    verbose_name_plural = _('вибрані атрибути у товарів в корзині')
  
  def __str__(self):
    return f'{self.cart_item.item.title}, {self.attribute_name.name}:{self.value.value}'




class FavourItem(models.Model):
  item = models.ForeignKey("sw_catalog.Item", on_delete=models.CASCADE, verbose_name='Улюблені товари', blank=True, null=True, related_name="favour_items")
  cart = models.ForeignKey('sw_cart.Cart', on_delete=models.CASCADE, verbose_name='Улюблені товари', blank=True, null=True, related_name="favour_items")
  
  def __str__(self):
    return f'{self.item.title}'

  class Meta:
    verbose_name=_("Улюблений товар")
    verbose_name_plural=_("Улюблені товари")



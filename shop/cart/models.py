from django.db import models 
from django.contrib.auth import get_user_model 
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from box.shop.item.models import Item, ItemCurrency 


User = get_user_model() 


class Cart(models.Model):
  user    = models.ForeignKey(verbose_name=_("Користувач"), to=User, on_delete=models.SET_NULL, related_name='carts', blank=True, null=True)
  order   = models.OneToOneField(verbose_name=_("Замовлення"), to="order.Order", blank=True, null=True, on_delete=models.CASCADE, related_name='cart')
  ordered = models.BooleanField(verbose_name=_("Замовлено"), default=False)
  created = models.DateTimeField(verbose_name=_('Дата створення'), default=timezone.now)
  updated = models.DateTimeField(verbose_name=_('Дата оновлення'),  auto_now_add=False, auto_now=True,  blank=True, null=True)

  def __str__(self):
    return f"{self.id}"
  
  class Meta:
    verbose_name = ('Корзина')
    verbose_name_plural = ('Корзини')
  
  def add_item(self, item_id, quantity):
    try: quantity = int(quantity)
    except: quantity = 1
    item = Item.objects.get(pk=int(item_id))
    cart_item, created = CartItem.objects.get_or_create(
      cart=self,
      item=item,
    )
    if created:
      cart_item.quantity = int(quantity)
    if not created:
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
      currency = currencies.first().name
    return currency


class CartItem(models.Model):
  ordered  = models.BooleanField( verbose_name=("Замовлено"), default=False)
  cart     = models.ForeignKey(   to='cart.Cart',   verbose_name=("Корзина"), on_delete=models.CASCADE, blank=True, null=True, related_name="items")
  order    = models.ForeignKey(   to='order.Order', verbose_name=('Замовлення'),   on_delete=models.CASCADE, blank=True, null=True, related_name="cart_items")
  item     = models.ForeignKey(   to='item.Item',   verbose_name=('Товар'),   on_delete=models.CASCADE, blank=True, null=True, related_name="cart_items")
  quantity = models.IntegerField(verbose_name=_('Кількість'), default=1)
  
  created  = models.DateTimeField(verbose_name=_('Дата создания'),  default=timezone.now)
  updated  = models.DateTimeField(verbose_name=_('Дата обновления'),auto_now_add=False, auto_now=True,  blank=True, null=True)

  @property
  def total_price(self):
    try:
      item = self.item.price
      if item:
        return item * self.quantity
      else:
        return None 
    except:
      print('Блядь поправ це гімно, відвалюється при покупці в 1 клік')
      return 1

  @property
  def price_per_item(self):
    return self.item.price

  @property
  def currency(self):
    return self.cart.currency

  def __str__(self):
    return f'{self.item.title}, {self.quantity}, {self.total_price} {self.item.currency}'

  class Meta: 
    verbose_name = ('Товар в корзині')
    verbose_name_plural = ('Товари в корзині')


class FavourItem(models.Model):
  item = models.ForeignKey('item.Item', on_delete=models.CASCADE, verbose_name='Улюблені товари', blank=True, null=True, related_name="favour_items")
  cart = models.ForeignKey('cart.Cart', on_delete=models.CASCADE, verbose_name='Улюблені товари', blank=True, null=True, related_name="favour_items")
  
  def __str__(self):
    return f'{self.item.name},{self.user}'

  class Meta:
    verbose_name=("Улюблений товар")
    verbose_name_plural=("Улюблені товари")



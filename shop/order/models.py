from django.db import models 
from django.contrib.auth import get_user_model 
from django.utils.translation import ugettext_lazy as _
from shop.cart.utils import get_cart
from .utils import send_order_mail 


User = get_user_model()


class OrderItemManager(models.Manager):
  def all(self):
    return super(OrderItemManager, self).get_queryset().filter(ordered=False)


class Status(models.Model):
  name = models.CharField(max_length=24, blank=True, null=True, default=None)
  is_active = models.BooleanField(default=True)
  created = models.DateTimeField(auto_now_add=True, auto_now=False)
  updated = models.DateTimeField(auto_now_add=False, auto_now=True)

  def __str__(self):
    return f"{self.name}"

  class Meta: 
    verbose_name = ('Статус')
    verbose_name_plural = ('Статуси')


class Order(models.Model):
  user = models.ForeignKey(verbose_name=("Юзер"), to=User, on_delete=models.SET_NULL, related_name='orders', blank=True, null=True)

  # cart        = models.OneToOneField(verbose_name=("Корзина"), to="cart.Cart", blank=True, null=True, on_delete=models.CASCADE, related_name='order')

  total_price = models.DecimalField(verbose_name=('Сумма замовлення'), max_digits=10, decimal_places=2, default=0)
  name        = models.CharField(verbose_name=('Імя'),                 max_length=120, blank=True, null=True)
  email       = models.CharField(verbose_name=("Е-майл"),              max_length=120, blank=True, null=True)
  phone       = models.CharField(verbose_name=('Номер телефона'),      max_length=120, blank=True, null=True)
  address     = models.CharField(verbose_name=('Адрес'),               max_length=120, blank=True, null=True)
  comments    = models.TextField(verbose_name=('Коментарии'),          blank=True, null=True, default=None)
  payment_opt = models.CharField(verbose_name=("Спосіб оплати"),       blank=True, null=True, max_length=120, help_text=' ')
  delivery_opt= models.CharField(verbose_name=("Спосіб доставки"),     blank=True, null=True, max_length=120)
  ordered     = models.BooleanField(verbose_name=('Заказ завершений'), default=False)
  status      = models.ForeignKey(verbose_name=('Статус'),  on_delete=models.CASCADE, to="Status", blank=True, null=True, related_name='orders') 
  created     = models.DateTimeField(verbose_name=('Дата создания'),   auto_now_add=True,  auto_now=False, blank=True, null=True)
  updated     = models.DateTimeField(verbose_name=('Дата обновления'), auto_now_add=False, auto_now=True,  blank=True, null=True)

  class Meta: 
    verbose_name = ('Замовлення товарів')
    verbose_name_plural = ('Замовлення товарів')

  def __str__(self):
    return f'{self.phone}|{self.name}|{self.email}|{self.address}' 

  def make_order_total_price(self):
    print(2)
    total_price = 0 
    for cart_item in self.cart_items.all():
      print(cart_item)
      total_price += cart_item.item.price * cart_item.quantity
    print(3)
    self.total_price = total_price
    self.save()


  def make_order(self, request):
    print('make_order')
    order = self
    order.ordered = True

    order.save()

    cart = get_cart(request)
    cart.ordered = True
    cart.items.all().update(ordered=True, order=order)
    cart.order = order 
    cart.save()

    if request.user.is_authenticated:
      order.user = request.user 
      cart.user  = request.user
      order.save()
      cart.save()
    print('1')
    self.make_order_total_price()
    send_order_mail()

from django.db import models 
from django.contrib.auth import get_user_model 
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from box.shop.cart.utils import get_cart
from box.shop.item.models import ItemStock 
from box.global_config.models import NotificationConfig
from box.core.mail import box_send_mail

from colorfield.fields import ColorField

from .managers import * 

User = get_user_model()



class Status(models.Model):
  action_choices = (
    (True,_("Списувати товар")),
    (False,_("Не списувати товар")),
  )
  color  = ColorField(verbose_name=("Колір"), blank=False, null=False)
  action = models.BooleanField(verbose_name=("Дія над товаром"), choices=action_choices, default=0)
  name   = models.CharField(verbose_name=("Назва"), max_length=255, blank=False, null=False)
  config = models.ForeignKey(to='order.OrderConfig', null=True, blank=False, on_delete=models.CASCADE)
  
  def __str__(self):
    return f"{self.name}"
  
  @classmethod 
  def modeltranslation_fields(cls):
    fields = [
      'name',
    ]
    return fields 

  class Meta: 
    verbose_name = ('статус замовленнь')
    verbose_name_plural = ('Статуси замовленнь')


class OrderTag(models.Model):
  color    = ColorField(verbose_name=("Колір"), )
  name     = models.CharField(verbose_name=("Назва"), max_length=255, blank=False, null=False)
  config = models.ForeignKey(to='order.OrderConfig', null=True, blank=False, on_delete=models.CASCADE)
  def __str__(self):
    return f"{self.name}"
  
  @classmethod 
  def modeltranslation_fields(cls):
    fields = [
    ]
    return fields 

  class Meta: 
    verbose_name = ('мітка замовленнь')
    verbose_name_plural = ('мітки замовленнь')


class Order(models.Model):
  user        = models.ForeignKey(verbose_name=("Користувач"), to=User, on_delete=models.SET_NULL, related_name='orders', blank=True, null=True)
  total_price = models.DecimalField(verbose_name=('Сумма замовлення'), max_digits=10, decimal_places=2, default=0)
  name        = models.CharField(verbose_name=('Імя'),                 max_length=255, blank=True, null=True)
  email       = models.CharField(verbose_name=("Е-майл"),              max_length=255, blank=True, null=True)
  phone       = models.CharField(verbose_name=('Номер телефона'),      max_length=255, blank=True, null=True)
  address     = models.CharField(verbose_name=('Адрес'),               max_length=255, blank=True, null=True)
  comments    = models.TextField(verbose_name=('Коментарии'),          blank=True, null=True)
  payment_opt = models.CharField(verbose_name=("Спосіб оплати"),       blank=True, null=True, max_length=255, help_text=' ')
  delivery_opt= models.CharField(verbose_name=("Спосіб доставки"),     blank=True, null=True, max_length=255)
  ordered     = models.BooleanField(verbose_name=('Завершено'), default=False)
  paid        = models.BooleanField(verbose_name=('Сплачено'),   default=False)
  note        = models.TextField(verbose_name=('Примітки адміністратора'), blank=True, null=True)
  status      = models.ForeignKey(verbose_name=('Статус'),  on_delete=models.CASCADE, to="order.Status", blank=False, null=True) 
  tags        = models.ManyToManyField(verbose_name=("Мітки"), blank=True, to="order.OrderTag")
  coupon      = models.ForeignKey(verbose_name=("Купон"), blank=True, null=True, to='customer.Coupon', on_delete=models.SET_NULL)
  objects     = OrderManager()
  is_active   = models.BooleanField(verbose_name=("Активність"),default=True)

  created     = models.DateTimeField(verbose_name=('Дата замовлення'),   default=timezone.now)
  updated     = models.DateTimeField(verbose_name=('Дата обовлення'), auto_now_add=False, auto_now=True,  blank=True, null=True)


  class Meta: 
    verbose_name = ('замовлення')
    verbose_name_plural = ('Список замовлень')
  
  def save(self, *args, **kwargs):
    if not self.status:
      if Status.objects.all().exists():
        self.status = Status.objects.all().first()
    super().save(*args, **kwargs)

  def __str__(self):
    return f'{self.phone}|{self.name}|{self.email}|{self.address}' 
  
  @property
  def currency(self):
    return self.cart.currency

  def make_order_total_price(self):
    # total_price = 0 
    # for cart_item in self.cart_items.all():
    #   total_price += cart_item.item.price * cart_item.quantity
    # self.total_price = total_price
    self.total_price = self.cart.total_price
    self.save()

  def make_order(self, request):
    order = self
    order.ordered = True
    order.save()
    cart = get_cart(request)
    cart.ordered = True
    # cart.items.all().update(ordered=True, order=order)
    unavailable_stocks = ItemStock.objects.filter(availability=False)
    for cart_item in cart.items.all():
      cart_item.ordered = True
      cart_item.order = order
      item = cart_item.item 
      if item.amount != None:
        if item.amount < cart_item.quantity:
          cart_item.quantity = item.amount 
          item.amount = 0 
          if unavailable_stocks.exists():
            item.in_stock = unavailable_stocks.first()
          else:
            item.in_stock = None 
        else:
          item.amount -= quantity 
      item.save()
      cart_item.save()
    cart.order = order 
    cart.save()

    if request.user.is_authenticated:
      order.user = request.user 
      cart.user  = request.user
      order.save()
      cart.save()
    self.make_order_total_price()
    config = NotificationConfig.get_solo()
    data = config.get_data('order')
    box_send_mail(
      subject=data['subject'],
      recipient_list=data['emails'],
      model=order
    )


class OrderRequest(models.Model):
    name    = models.CharField(verbose_name=("Ім'я"),         max_length=255, blank=True, null=True)
    surname = models.CharField(verbose_name=("Фамілія"),      max_length=255, blank=True, null=True)
    phone   = models.CharField(verbose_name=("Телефон"),      max_length=255, blank=True, null=True)
    email   = models.CharField(verbose_name=("Емайл"),        max_length=255, blank=True, null=True)
    item    = models.ForeignKey(verbose_name=("Товар"),       blank=True, null=True, on_delete=models.CASCADE, to="item.Item")
    created = models.DateTimeField(verbose_name=("Створено"), blank=True, null=True, default=timezone.now)
    
    def __str__(self):
        return f"{self.name}, {self.email}, {self.phone}"

    class Meta:
        verbose_name = 'Покупка в один клік'
        verbose_name_plural = 'покупки в 1 клік'


class ItemRequest(models.Model):
    name    = models.CharField(verbose_name=("Ім'я"),         max_length=255, blank=True, null=True)
    phone   = models.CharField(verbose_name=("Телефон"),      max_length=255, blank=True, null=True)
    email   = models.CharField(verbose_name=("Емайл"),        max_length=255, blank=True, null=True)
    message = models.TextField(verbose_name=("Повідомлення"), blank=True, null=True)
    item    = models.ForeignKey(verbose_name=("Товар"),       blank=True, null=True, on_delete=models.CASCADE, to="item.Item")
    created = models.DateTimeField(verbose_name=("Створено"), blank=True, null=True, default=timezone.now)
    
    def __str__(self):
        return f"{self.name}, {self.email}, {self.phone}"

    class Meta:
        verbose_name = 'Заявка на інформацію про товар'
        verbose_name_plural = 'Заявки на інформацію про товар'

from box.solo.models import SingletonModel

class OrderConfig(SingletonModel):
  def __str__(self):
    return f'{self.id}'
  class Meta:
    verbose_name = _("Налаштування замовленя")
    verbose_name_plural = verbose_name
    


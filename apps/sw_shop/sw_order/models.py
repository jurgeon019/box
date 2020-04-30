from django.db import models 
from django.contrib.auth import get_user_model 
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from box.apps.sw_shop.sw_cart.models import CartItem
from box.apps.sw_shop.sw_cart.utils import get_cart
from box.apps.sw_shop.sw_catalog.models import ItemStock 
from box.core.sw_global_config.models import NotificationConfig
from box.core.mail import box_send_mail

from colorfield.fields import ColorField


User = get_user_model()


class Order(models.Model):
  user        = models.ForeignKey(verbose_name=_("Користувач"), to=User, on_delete=models.SET_NULL, related_name='orders', blank=True, null=True)
  total_price = models.DecimalField(verbose_name=_('Сумма замовлення'), max_digits=10, decimal_places=2, default=0)
  name        = models.CharField(verbose_name=_('Імя'),                 max_length=255, blank=True, null=True)
  email       = models.CharField(verbose_name=_("Е-майл"),              max_length=255, blank=True, null=True)
  phone       = models.CharField(verbose_name=_('Номер телефона'),      max_length=255, blank=True, null=True)
  address     = models.CharField(verbose_name=_('Адрес'),               max_length=255, blank=True, null=True)
  comments    = models.TextField(verbose_name=_('Коментарии'),          blank=True, null=True)
  payment_opt = models.CharField(verbose_name=_("Спосіб оплати"),       blank=True, null=True, max_length=255, help_text=' ')
  delivery_opt= models.CharField(verbose_name=_("Спосіб доставки"),     blank=True, null=True, max_length=255)
  ordered     = models.BooleanField(verbose_name=_('Завершено'), default=False)
  paid        = models.BooleanField(verbose_name=_('Сплачено'),   default=False)
  note        = models.TextField(verbose_name=_('Примітки адміністратора'), blank=True, null=True)
  status      = models.ForeignKey(verbose_name=_('Статус'),  on_delete=models.CASCADE, to="sw_order.Status", blank=False, null=True) 
  tags        = models.ManyToManyField(verbose_name=_("Мітки"), blank=True, to="sw_order.OrderTag")
  coupon      = models.ForeignKey(verbose_name=_("Купон"), blank=True, null=True, to='sw_customer.Coupon', on_delete=models.SET_NULL)
  is_active   = models.BooleanField(verbose_name=_("Активність"), default=True, help_text=_("Замість видалення цей флаг проставляється в False"))
  created     = models.DateTimeField(verbose_name=_('Дата замовлення'), default=timezone.now)
  updated     = models.DateTimeField(verbose_name=_('Дата оновлення'), auto_now_add=False, auto_now=True,  blank=True, null=True)


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
  
  def handle_amount(self, request):
    order = self
    cart = get_cart(request)
    # unavailable_stocks = ItemStock.objects.filter(availability=False)
    unavailable_stock = ItemStock.objects.filter(availability=False).first()
    
    # for cart_item in cart.items.all():
    for cart_item in CartItem.objects.filter(cart=cart):
      cart_item.ordered = True
      cart_item.order = order
      item = cart_item.item 
      if item.amount != None:
        if item.amount < cart_item.quantity:
          cart_item.quantity = item.amount 
          item.amount = 0 
          # if unavailable_stocks.exists():
          #   item.in_stock = unavailable_stocks.first()
          # else:
          #   item.in_stock = None 
          item.in_stock = unavailable_stock
        else:
          item.amount -= cart_item.quantity 
      item.save()
      cart_item.save()

  def handle_user(self, request):
    cart = get_cart(request)
    if request.user.is_authenticated:
      self.user = request.user 
      self.save()
      cart.user  = request.user
      cart.save()
  
  def make_order(self, request):
    cart = get_cart(request)
    self.handle_user(request)
    self.handle_amount(request)
    self.total_price = self.cart.total_price
    self.ordered = True
    self.save()
    cart.order = self 
    cart.ordered = True
    cart.save()
    config = NotificationConfig.get_solo()
    data = config.get_data('order')
    box_send_mail(
      subject=data['subject'],
      recipient_list=data['emails'],
      model=self
    )


class ItemRequest(models.Model):
    name    = models.CharField(verbose_name=_("Ім'я"),         max_length=255, blank=True, null=True)
    phone   = models.CharField(verbose_name=_("Телефон"),      max_length=255, blank=True, null=True)
    email   = models.CharField(verbose_name=_("Емайл"),        max_length=255, blank=True, null=True)
    message = models.TextField(verbose_name=_("Повідомлення"), blank=True, null=True)
    item    = models.ForeignKey(verbose_name=_("Товар"),       blank=True, null=True, on_delete=models.CASCADE, to="sw_catalog.Item")
    created = models.DateTimeField(verbose_name=_("Створено"), blank=True, null=True, default=timezone.now)
    
    def __str__(self):
        return f"{self.name}, {self.email}, {self.phone}"

    class Meta:
        verbose_name = 'Заявка на інформацію про товар'
        verbose_name_plural = 'Заявки на інформацію про товар'

from box.core.sw_solo.models import SingletonModel

class OrderConfig(SingletonModel):
  def __str__(self):
    return f'{self.id}'
  class Meta:
    verbose_name = _("Налаштування замовленя")
    verbose_name_plural = verbose_name
    




class Status(models.Model):
  # action_choices = (
  #   (True,_("Списувати товар")),
  #   (False,_("Не списувати товар")),
  # )
  # action = models.BooleanField(verbose_name=_("Дія над товаром"), choices=action_choices, default=0)
  color  = ColorField(verbose_name=_("Колір"), blank=False, null=False)
  name   = models.CharField(verbose_name=_("Назва"), max_length=255, blank=False, null=False)
  config = models.ForeignKey(to='sw_order.OrderConfig', null=True, blank=True, on_delete=models.CASCADE)
  
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
  color    = ColorField(verbose_name=_("Колір"), )
  name     = models.CharField(verbose_name=_("Назва"), max_length=255, blank=False, null=False)
  config = models.ForeignKey(to='sw_order.OrderConfig', null=True, blank=False, on_delete=models.CASCADE)
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


from django.db import models 
from django.contrib.auth import get_user_model 
from django.utils.translation import ugettext_lazy as _
from box.shop.cart.utils import get_cart
from .utils import send_order_mail 
from django.utils import timezone

User = get_user_model()


class OrderManager(models.Manager):
  def all(self):
    # return super(OrderManager, self).get_queryset().filter(ordered=False)
    return super(OrderManager, self).get_queryset().filter(is_active=True)


class Status(models.Model):
  name      = models.CharField(verbose_name=("Статус"), max_length=255, blank=False, null=False)
  
  def __str__(self):
    return f"{self.name}"

  class Meta: 
    verbose_name = ('Статус замовлення')
    verbose_name_plural = ('Статуси замовлення')


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
  ordered     = models.BooleanField(verbose_name=('Завершений'), default=False)
  status      = models.ForeignKey(verbose_name=('Статус'),  on_delete=models.CASCADE, to="Status", blank=False, null=True, related_name='orders') 
  is_active   = models.BooleanField(default=True)
  
  objects     = OrderManager()

  created     = models.DateTimeField(verbose_name=('Дата створення'),   default=timezone.now)
  updated     = models.DateTimeField(verbose_name=('Дата обовлення'), auto_now_add=False, auto_now=True,  blank=True, null=True)

  class Meta: 
    verbose_name = ('Замовлення товарів')
    verbose_name_plural = ('Замовлення товарів')
  
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
    from box.shop.item.models import ItemStock 
    unavailable_stocks = ItemStock.objects.filter(available=False)
    for cart_item in cart.items.all():
      cart_item.ordered = True
      cart_item.order = order
      item = cart_item.item 
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
    cart.order = order 
    cart.save()

    if request.user.is_authenticated:
      order.user = request.user 
      cart.user  = request.user
      order.save()
      cart.save()
    self.make_order_total_price()
    model = order 
    from django.shortcuts import reverse 
    from django.conf import settings 
    from django.core.mail import send_mail
    link  = reverse(f'admin:{model._meta.app_label}_{model._meta.model_name}_change', args=(model.id,))
    send_mail(
      subject = 'Отримано замовлення',
      # message = get_template('contact_message.txt').render({'message':message}),
      message = settings.CURRENT_DOMEN+link,
      from_email = settings.EMAIL_HOST_USER,
      recipient_list = [settings.EMAIL_HOST_USER],
      fail_silently=False,
      # fail_silently=True,
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





from django.db import models 
from django.contrib.auth import get_user_model 
from django.utils.translation import ugettext_lazy as _


User = get_user_model() 


class Cart(models.Model):
	user    = models.ForeignKey(verbose_name=("Юзер"), to=User, on_delete=models.SET_NULL, related_name='carts', blank=True, null=True)
	order   = models.OneToOneField(verbose_name=("Замовлення"), to="order.Order", blank=True, null=True, on_delete=models.CASCADE, related_name='cart')
	ordered = models.BooleanField(verbose_name=("Замовлено"), default=False)
	created = models.DateTimeField(verbose_name=('Дата створення'),  auto_now_add=True,  auto_now=False, blank=True, null=True)
	updated = models.DateTimeField(verbose_name=('Дата оновлення'),  auto_now_add=False, auto_now=True,  blank=True, null=True)

	def __str__(self):
		return f"{self.id}"
	
	class Meta:
		verbose_name = ('Корзина')
		verbose_name_plural = ('Корзини')

	@property
	def total_price(self):
		total_price = 0
		for cart_item in self.items.all():
			total_price += cart_item.total_price
		return total_price

	def add_to_cart(self, slug):
		cart = self
		product = Product.objects.get(slug=slug)
		new_item,  = CartItem.objects.get_or_create(product=product, item_total=product.price)
		cart_items = [item.product for item in cart.items.all()]
		if new_item.product not in cart_items:
			cart.items.add(new_item)
			cart.save()

	def remove_from_cart(self, slug):
		cart = self
		product = Product.objects.get(slug=slug)
		for cart_item in cart.items.all():
			if cart_item.product == product:
				cart.items.remove(cart_item)
				cart.save()

	def change_qty(self, qty, id):
		cart = self
		cart_item = CartItem.objects.get(id=int(id))
		cart_item.qty = int(qty)
		cart_item.item_total = int(qty) * Decimal(cart_item.product.price)
		cart_item.save()
		new_cart_total = 0.00
		for item in cart.items.all():
			new_cart_total += float(item.item_total)
		cart.cart_total = new_cart_total
		cart.save()


class CartItem(models.Model):
  ordered  = models.BooleanField( verbose_name=("Замовлено"), default=False)
  cart     = models.ForeignKey(   to='cart.Cart',   verbose_name=("Корзина"), on_delete=models.CASCADE, blank=True, null=True, related_name="items")
  order    = models.ForeignKey(   to='order.Order', verbose_name=('Замовлення'),   on_delete=models.CASCADE, blank=True, null=True, related_name="cart_items")
  item     = models.ForeignKey(   to='item.Item',   verbose_name=('Товар'),   on_delete=models.CASCADE, blank=True, null=True, related_name="cart_items")
  quantity = models.IntegerField(verbose_name=('Кількість'), default=1)
  
  created  = models.DateTimeField(verbose_name=('Дата создания'),  auto_now_add=True,  auto_now=False, blank=True, null=True)
  updated  = models.DateTimeField(verbose_name=('Дата обновления'),auto_now_add=False, auto_now=True,  blank=True, null=True)

  @property
  def total_price(self):
	  return self.item.price * self.quantity
	
  @property
  def price_per_item(self):
	  return self.item.price
	
  def __str__(self):
	  return f'{self.item.title}, {self.quantity}штука, {self.total_price} {self.item.currency}'

  class Meta: 
    verbose_name = ('Товар в корзині')
    verbose_name_plural = ('Товари в корзинах')


class FavourItem(models.Model):
  item = models.ForeignKey('item.Item', on_delete=models.CASCADE, verbose_name='Улюблені товари', blank=True, null=True, related_name="favour_items")
  cart = models.ForeignKey('cart.Cart', on_delete=models.CASCADE, verbose_name='Улюблені товари', blank=True, null=True, related_name="favour_items")
  
  def __str__(self):
    return f'{self.item.name},{self.user}, {self.sk}'

  class Meta:
    verbose_name=("Улюблений товар")
    verbose_name_plural=("Улюблені товари")
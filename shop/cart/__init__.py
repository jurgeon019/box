from django import apps 


class CartConfig(apps.AppConfig):
    name = 'box.shop.cart'
    verbose_name = "корзина"

default_app_config = 'box.shop.cart.CartConfig'



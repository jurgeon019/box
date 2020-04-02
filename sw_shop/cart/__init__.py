from django import apps 


class CartConfig(apps.AppConfig):
    name = 'box.sw_shop.cart'
    verbose_name = "корзина"

default_app_config = 'box.sw_shop.cart.CartConfig'



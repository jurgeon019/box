from django import apps 


class CartConfig(apps.AppConfig):
    name = 'box.apps.sw_shop.cart'
    verbose_name = "корзина"

default_app_config = 'box.apps.sw_shop.cart.CartConfig'



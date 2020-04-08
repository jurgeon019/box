from django import apps 


class OrderConfig(apps.AppConfig):
    name                = 'box.sw_shop.order'
    verbose_name        = 'Замовлення'
    verbose_name_plural = verbose_name



default_app_config = 'box.sw_shop.order.OrderConfig'


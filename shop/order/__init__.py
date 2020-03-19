from django import apps 


class OrderConfig(apps.AppConfig):
    name                = 'box.shop.order'
    verbose_name        = 'Замовлення'
    verbose_name_plural = verbose_name



default_app_config = 'box.shop.order.OrderConfig'


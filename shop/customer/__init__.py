from django import apps 



class ProfileConfig(apps.AppConfig):
    name = 'box.shop.customer'
    verbose_name = 'Покупці'
    

default_app_config = 'box.shop.customer.ProfileConfig'
    
from django import apps 


class BlogConfig(apps.AppConfig):
    name = 'box.apps.sw_blog'
    verbose_name = 'блог'
    
    
default_app_config = 'box.apps.sw_blog.BlogConfig'



from django import apps 


class BlogConfig(apps.AppConfig):
    name = 'box.sw_blog'
    verbose_name = 'блог'
    
    
default_app_config = 'box.sw_blog.BlogConfig'



from django.db.models.signals import post_save




def func(sender, instance, **kwargs):
    print(sender, instance, kwargs)




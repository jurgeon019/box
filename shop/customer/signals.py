from django.db.models.signals import post_save
from django.dispatch import receiver
from box.shop.customer.models import Customer



User = get_user_model()

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)
    instance.customer.save()



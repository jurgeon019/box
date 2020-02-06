from django.db.models.signals import post_save
from django.dispatch import receiver
from box.shop.profile.models import Profile



User = get_user_model()

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()



from .models import NotificationConfig
from django.urls import reverse


def get_configuration_admin_url():
    meta = NotificationConfig._meta
    return reverse('admin:{}_{}_change'.format(
        meta.app_label, meta.model_name
    ))

__all__ = ['get_configuration_admin_url']

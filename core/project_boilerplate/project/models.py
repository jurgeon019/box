from django.db import models
from box.custom_auth.models import User as BoxUser


class User(BoxUser):
    pass 

class ContactForm(models.Model):
    name    = models.CharField(verbose_name='name', blank=True, null=True, max_length=255)
    email   = models.CharField(verbose_name='email', blank=True, null=True, max_length=255)
    phone   = models.CharField(verbose_name='phone', blank=True, null=True, max_length=255)
    message = models.TextField(verbose_name='message', blank=True, null=True)

    def __str__(self):
        return f"{self.name}, {self.email}, {self.phone}, {self.message}"

    class Meta:
        verbose_name = 'заявка на консультацію'
        verbose_name_plural = 'заявки на консультацію'
        



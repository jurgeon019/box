from django.db import models 
from django.contrib.auth.models import User, AbstractBaseUser,AbstractUser



class User(AbstractUser):
  phone_number = models.CharField(verbose_name=("Номер телефону"), max_length=255, blank=True, null=True)
  
  def __str__(self):
    return f"{self.first_name} {self.last_name} ({self.username}, {self.phone_number}, {self.email})"
  
  class Meta:
    verbose_name = ('Користувач')
    verbose_name_plural = ('Користувачі')



from django.db import models 
from django.contrib.auth.models import User, AbstractBaseUser,AbstractUser



class User(AbstractUser):
  phone_number = models.CharField(("Phone Number"), max_length=50, default='')

  def __str__(self):
    return f"{self.phone_number}"
  
  class Meta:
    verbose_name = 'Користувач'
    verbose_name_plural = 'Користувачі'


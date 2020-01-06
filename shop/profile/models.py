from django.contrib.auth import get_user_model 
from django.db import models 



User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = 'Профіль'
        verbose_name_plural = 'Профілі'
    
    
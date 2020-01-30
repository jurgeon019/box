from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User 


class Command(BaseCommand):
  def handle(self, *args, **kwargs):
    User = get_user_model()
    username = 'admin'
    password = 'motto2109'
    email    = ''
    try:
        User.objects.create_superuser(
            username = username, 
            email    = email, 
            password = password,
        )
        print('user has been created')
    except:
        user = User.objects.get(
            username=username,
        )
        user.set_password(password)
        print('password has been set')
        print(user.username)
        print(user.password)
        user.save()
    self.stdout.write(self.style.SUCCESS('Data imported successfully'))


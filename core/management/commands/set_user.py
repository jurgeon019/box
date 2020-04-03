from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User 


class Command(BaseCommand):

  def add_arguments(self, parser):
      parser.add_argument(
          'username',
          type=str,
          help='Username',
      )
      parser.add_argument(
          'password',
          type=str,
          help='Password',
      )
      parser.add_argument(
          'email',
          type=str,
          help='Email',
      )

  
  def handle(self, *args, **kwargs):
    User = get_user_model()
    username = kwargs['username']
    password = kwargs['password']
    email    = kwargs['email']
    try:
        User.objects.filter(username=username)
        User.objects.create_superuser(
            username = username, 
            email    = email, 
            password = password,
        )
        print('user has been created')
    except Exception as e :
        print(e)
        user = User.objects.get(
            username=username,
        )
        print(user)
        user.set_password(password)
        user.email = email
        user.save()
        print('password has been set')
        print(user.username)
        print(user.password)
        user.save()
    self.stdout.write(self.style.SUCCESS('Data imported successfully'))



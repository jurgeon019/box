from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User 


class Command(BaseCommand):

  def add_arguments(self, parser):
      parser.add_argument(
          'username',
      )
      parser.add_argument(
          'password',
      )
      parser.add_argument(
          'email',
      )
      parser.add_argument(
          'phone_number',
      )
      parser.add_argument(
          'first_name',
      )
      parser.add_argument(
          'last_name',
      )

  def handle(self, *args, **kwargs):
    User = get_user_model()
    username      = kwargs['username']
    password      = kwargs['password']
    email         = kwargs['email']
    phone_number  = kwargs['phone_number']
    first_name    = kwargs['first_name']
    last_name     = kwargs['last_name']
    try:
        User.objects.filter(username=username)
        User.objects.create_superuser(
            username     = username, 
            email        = email, 
            password     = password,
            phone_number = phone_number,
            first_name   = first_name,
            last_name    = last_name,
        )
        print('user has been created')
    except Exception as e :
        print(e)
        user = User.objects.get(
            username=username,
        )
        print(user)
        user.set_password(password)
        user.email        = email
        user.password     = password
        user.phone_number = phone_number
        user.first_name   = first_name
        user.last_name    = last_name

        user.save()
        print('password has been set')
        print(user.username)
        print(user.password)
        user.save()
    self.stdout.write(self.style.SUCCESS('Data imported successfully'))



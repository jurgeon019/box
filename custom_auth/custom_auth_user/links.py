khttps://docs.djangoproject.com/en/2.2/topics/auth/
https://docs.djangoproject.com/en/2.2/topics/auth/default/
https://docs.djangoproject.com/en/2.2/ref/contrib/auth/
https://docs.djangoproject.com/en/2.2/topics/auth/customizing/
https://docs.djangoproject.com/en/2.2/topics/auth/passwords/


# python manage.py createsuperuser --username=joe --email=joe@example.com
# manage.py changepassword *username*
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Permission
from django.contrib.auth import authenticate, login, logout
from myapp.models import BlogPost
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, staff_member_required, user_passes_test, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin, 
from django.contrib.auth.models import User


user = User.objects.create_user('john', 
'lennon@thebeatles.com', 'johnpassword')
user.first_name = 'John'
user.last_name = 'Lennon'
user.save()
u = User.objects.get(username='john')
u.set_password('new password')
u.save()
user = authenticate(request, username='john', password='secret')
if user is not None:
    # A backend authenticated the credentials
else:
    # No backend authenticated the credentials

# Permissions
# has_view_permission(), 
# has_add_permission(), 
# has_change_permission()
# has_delete_permission() 
myuser.groups.set([group_list])
myuser.groups.add(group, group, ...)
myuser.groups.remove(group, group, ...)
myuser.groups.clear()
myuser.user_permissions.set([permission_list])
myuser.user_permissions.add(permission, permission, ...)
myuser.user_permissions.remove(permission, permission, ...)
myuser.user_permissions.clear()

# Для прокси:
# content_type = ContentType.objects.get_for_model(BlogPostProxy, for_concrete_model=False)
content_type = ContentType.objects.get_for_model(BlogPost)
permission = Permission.objects.create(
    codename='can_publish',
    name='Can Publish Posts',
    content_type=content_type,
)
# The permission can then be assigned to a User via its user_permissions attribute or to a Group via its permissions attribute.

# app_label=foo, model=Bar
# add: user.has_perm('foo.add_bar')
# change: user.has_perm('foo.change_bar')
# delete: user.has_perm('foo.delete_bar')
# view: user.has_perm('foo.view_bar')
def user_gains_perms(request, user_id):
  user = get_object_or_404(User, pk=user_id)
  user.has_perm('myapp.change_blogpost') # # any permission check will cache the current set of permissions,
  content_type = ContentType.objects.get_for_model(BlogPost)
  permission = Permission.objects.get(codename='change_blogpost',content_type=content_type,)
  user.user_permissions.add(permission)
  # Checking the cached permission set
  user.has_perm('myapp.change_blogpost')  # False - 
  user = get_object_or_404(User, pk=user_id) # Request new instance of User. user.refresh_from_db() won't clear the cache.
  user.has_perm('myapp.change_blogpost')  # True - Permission cache is repopulated from the database
  # ...


# Proxy models
class Person(models.Model):
  class Meta:
    permissions = [('can_eat_pizzas', 'Can eat pizzas')]

class Student(Person):
  class Meta:
    proxy = True # Proxy models don’t inherit the permissions of the concrete model they subclass:
    permissions = [('can_deliver_pizzas', 'Can deliver pizzas')]
# Fetch the content type for the proxy model.
content_type = ContentType.objects.get_for_model(Student, for_concrete_model=False)
student_permissions = Permission.objects.filter(content_type=content_type)
print([p.codename for p in student_permissions])
# >>> ['add_student', 'change_student', 'delete_student', 'view_student', 'can_deliver_pizzas']
for permission in student_permissions:
    user.user_permissions.add(permission)
user.has_perm('app.add_person')
False
user.has_perm('app.can_eat_pizzas')
False
user.has_perms(('app.add_student', 'app.can_deliver_pizzas'))
True

# Authentication in Web requests

def login_view(request):
  username = request.POST['username']
  password = request.POST['password']
  user = authenticate(request, username=username, password=password)
  if user is not None:
    login(request, user)
    # Redirect to a success page.
    # ...
  else:
    # Return an 'invalid login' error message.
    # ...
      
def logout_view(request):
    logout(request)
    # Redirect to a success page.



def my_view(request):
  if not request.user.email.endswith('@example.com'):
        return redirect('/login/?next=%s' % request.path)
  if not request.user.is_authenticated:
    return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    # return render(request, 'myapp/login_error.html')
  # ...

@login_required(login_url='/accounts/login/', redirect_field_name='next')
def my_view(request):
    # ...

class MyView(LoginRequiredMixin, View):
  login_url = '/login/'
  redirect_field_name = 'redirect_to'



def my_view(request):
  if not request.user.email.endswith('@example.com'):
    return redirect('/login/?next=%s' % request.path)

def email_check(user):
  return user.email.endswith('@example.com')

@user_passes_test(email_checklogin_url='/accounts/login/', redirect_field_name='next')
def my_view(request):
  # ...


class MyView(UserPassesTestMixin, View):
  def test_func(self):
    return self.request.user.email.endswith('@example.com')


class TestMixin1(UserPassesTestMixin):
  def test_func(self):
    return self.request.user.email.endswith('@example.com')

class TestMixin2(UserPassesTestMixin):
  def test_func(self):
    return self.request.user.username.startswith('django')

class MyView(TestMixin1, TestMixin2, View):
  # ...

# <app label>.<permission_codename>
@login_required
@permission_required('polls.can_vote', login_url='/loginpage/', raise_exception=True)
def my_view(request):
  # ...

class MyView(PermissionRequiredMixin, View):
  permission_required = 'polls.can_vote'
  # Or multiple of permissions:
  permission_required = ('polls.can_open', 'polls.can_edit')


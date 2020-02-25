from django.utils import translation
from django.shortcuts import redirect


from django.utils.safestring import mark_safe
from django.contrib.admin.widgets import AdminFileWidget


class AdminImageWidget(AdminFileWidget):
  def render(self, name, value, attrs=None, renderer=None):
    output = []
    if value and getattr(value, "url", None):
      image_url = value.url
      file_name = str(value)
      output.append(
        f' <a href="{image_url}" target="_blank">'
        f'  <img src="{image_url}" alt="{file_name}" width="150" height="150" '
        f'style="object-fit: cover;"/> </a>')
    output.append(super(AdminFileWidget, self).render(name, value, attrs, renderer))
    return mark_safe(u''.join(output))




def set_lang(request, lang=None):
  # lang = request.POST['lang']
  translation.activate(lang)
  request.session[translation.LANGUAGE_SESSION_KEY] = lang
  # return redirect(request.META['HTTP_REFERER'])
  url = request.META['HTTP_REFERER'].split('/')
  url[3] = lang
  url = '/'.join(url)
  print(lang)
  return redirect(url)


def get_sk(request):
  sk = request.session.session_key
  if not sk: 
    request.session.cycle_key()
  return sk 


def get_user(request):
  if request.user.is_anonymous:
    return None
  return request.user


def get_line():
  import inspect 
  caller = inspect.getframeinfo(inspect.stack()[1][0])
  print(caller)
  # print('filename:', inspect.getframeinfo(inspect.currentframe()).filename)
  # print('line:', inspect.getframeinfo(inspect.currentframe()).lineno)

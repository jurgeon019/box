from django.utils import translation
from django.shortcuts import redirect



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

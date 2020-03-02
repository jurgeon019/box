from django.http import JsonResponse, JsonResponse 
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib.auth import (authenticate, get_user_model, login, logout)
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse 
from django.contrib import messages 


User = get_user_model()


@csrf_exempt 
def custom_login(request):

    response    = redirect(request.META['HTTP_REFERER'])
    username    = request.POST['username']
    password    = request.POST['password']
    remember_me = request.GET.get('remember_me')

    if remember_me == "true":
        pass
    else:
        request.session.set_expiry(0)
    
    user = User.objects.filter(
        Q(username__iexact=username)|
        Q(email__iexact=username)
    ).distinct() 

    if not user.exists() and user.count() != 1:
        message = 'Такого користувача не існує'
        print(message)
        # if request.is_ajax():
        if True:
            response = JsonResponse({
                'message':message,
                'status':'BAD',
            })
        messages.success(request, message)
        return response

    user = user.first() 

    if not user.check_password(password):
        return JsonResponse({
            'message':'Неправильний пароль',
            'status':'BAD',
        })

    if not user.is_active:
        message = 'Цей користувач неактивний'
        print(message)
        # if request.is_ajax():
        if True:
            response = JsonResponse({
                'message':message,
                'status':'BAD',
            })
        messages.success(request, message)
        return response

    user = authenticate(username=user.username, password=password)

    # if user is not None:
    #     if user.is_active:
    #         login(request, user)
    #         return JsonResponse('fine')
    #     else:
    #         return JsonResponse('inactive')
    # else:
    #     return JsonResponse('bad')

    login(request, user)

    message = 'Ви увійшли'
    print(message)
    # if request.is_ajax():
    if True:
        response = JsonResponse({
            'status':'OK',
            'message':message,
            'is_authenticated':request.user.is_authenticated,
            # 'url':reverse('index'),
            'url':reverse('profile'),
        })
    messages.success(request, message)
    return response


@csrf_exempt 
def custom_logout(request):
    response = redirect(request.META['HTTP_REFERER'])
    logout(request)
    # if request.is_ajax():
    if True:
        response = JsonResponse({
            'status':'OK',
            'message':'Ви вийшли',
            'is_authenticated':request.user.is_authenticated,
            'url':reverse('index')
        })
    return response


@csrf_exempt 
def custom_register(request):
    query = request.POST
    if not query:
        query = request.GET
    response   = redirect(request.META['HTTP_REFERER'])

    username   = query['username']

    password   = query['password']
    password2  = query['password2']

    email      = query.get('email','')
    email2     = query.get('email2','')

    first_name = query.get('first_name','')
    last_name  = query.get('last_name','')

    phone      = query.get('phone', '')
  
    if email and email2 and email != email2:
        message = 'Email must match'
        print(message)
        # if request.is_ajax():
        if True:
          response = JsonResponse({
            'status':'BAD',
            'message':message,
          })
        return response
      
    if password and password2 and password != password2:
        message = 'Паролі мусять співпадати'
        print(message)
        # if request.is_ajax():
        if True:
            response = JsonResponse({
                'status':'BAD',
                'message':message,
            })
        messages.success(request, message)
        return response 
    
    email_qs    = User.objects.filter(email=email)
    username_qs = User.objects.filter(username=username)

    if email_qs.exists() and email != '' and username_qs.exists() and username != '':
        message = 'Цей емайл та пароль вже використали для реєстрації'
        print(message)
        # if request.is_ajax():
        if True:
            response = JsonResponse({
                'status':'BAD',
                'message':message,
            })
        messages.success(request, message)
        return response 

    if email_qs.exists() and email != '':
        message = 'Цей емайл вже був використаний'
        print(message)
        # if request.is_ajax():
        if True:
            response = JsonResponse({
                'status':'BAD',
                'message':message,
            })
        messages.success(request, message)
        return response

    if username_qs.exists() and username != '':
        message = 'Це імя користувача вже було використано'
        print(message)
        # if request.is_ajax():
        if True:
            response = JsonResponse({
                'status':'BAD',
                'message':message,
            })
        messages.success(request, message)
        return response

    user = User.objects.create_user(
        username     = username,
        email        = email, 
        first_name   = first_name, 
        last_name    = last_name, 
        phone_number = phone,
    )
    user.set_password(password)
    # user.is_active = False 
    # TODO: custom email confirmation 
    user.save() 
    new_user = authenticate(username=user.username, password=password)
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
  
    # if request.is_ajax():
    if True:
        response = JsonResponse({
            'status':'OK',
            'message':('Вас було зареєстровано'),
            'is_authenticated':request.user.is_authenticated,
            'url':reverse('index'),
        })
    return response



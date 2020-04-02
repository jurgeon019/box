from django.http import JsonResponse, HttpResponse 
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib.auth import (authenticate, get_user_model, login, logout)
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse 
from django.contrib import messages 
from django.utils.translation import gettext_lazy as _


from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import viewsets


from .serializers import *
from ..settings import LOGIN_REDIRECT_URL


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)
    
    def create(self, request, *args, **kwargs):
        # https://stackoverflow.com/questions/16857450/how-to-register-users-in-django-rest-framework
        # TODO: розібратись як зробити нормально, так шоб видавались поля які мають бути заповнені, і з валідацією, **validated_data

        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        query       = request.data
        sw_register_(query)


def current_user(request):
    return JsonResponse(UserSerializer(request.user, many=False).data, safe=False)


@csrf_exempt 
def sw_login(request):
    query = request.POST or request.GET
    response    = redirect(request.META['HTTP_REFERER'])
    username    = query['username']
    password    = query['password']
    remember_me = request.GET.get('remember_me')

    if remember_me == "true":
        pass
    else:
        request.session.set_expiry(0)
    
    user = get_user_model().objects.filter(
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
    return JsonResponse({
        'status':'OK',
        'message':_('Ви увійшли'),
        'url':reverse(auth_settings.LOGIN_REDIRECT_URL),
    })


@csrf_exempt 
def sw_logout(request):
    logout(request)
    return JsonResponse({
        'status':'OK',
        'url':request.META.get('HTTP_REFERER', '/'),
    })


def sw_register(request):
    query = request.POST or request.GET
    return _sw_register(query)

def _sw_register(query):
    username    = query['username']
    password    = query['password']
    password2   = query['password2']
    email       = query.get('email','')
    email2      = query.get('email2','')
    first_name  = query.get('first_name','')
    last_name   = query.get('last_name','')
    phone       = query.get('phone', '')
    email_qs    = get_user_model().objects.filter(email=email)
    username_qs = get_user_model().objects.filter(username=username)

    if email and email2 and email != email2:
        return JsonResponse({
            'status':'BAD',
            'message':_('Email must match'),
        })
    if password and password2 and password != password2:
        return JsonResponse({
            'status':'BAD',
            'message':_('Passwords must match'),
        }) 
    if email_qs.exists() and email != '' and username_qs.exists() and username != '':
        return JsonResponse({
            'status':'BAD',
            'message':_('Email and username has already been used.'),
        }) 
    if email_qs.exists() and email != '':
        return JsonResponse({
            'status':'BAD',
            'message':_('Email has already been used.'),
        })
    if username_qs.exists() and username != '':
        return JsonResponse({
            'status':'BAD',
            'message':_('Username has already been used.'),
        })
    user = get_user_model().objects.create_user(
        username     = username,
        email        = email, 
        first_name   = first_name, 
        last_name    = last_name, 
        phone_number = phone,
    )
    user.set_password(password)
    user.is_active = True 
    # user.is_active = False 
    # TODO: custom email confirmation 
    user.save() 
    new_user = authenticate(username=user.username, password=password)
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return JsonResponse({
        'status':'OK',
        'url':request.META.get('HTTP_REFERER', '/'),
    })

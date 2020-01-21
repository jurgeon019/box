from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.db.models import Q

from core.models import Page


def index(request):
  # page = Page.objects.get(code='index')
  page, _ = Page.objects.get_or_create(code='index')
  return render(request, 'index.html', locals())


def about(request):
  # page = Page.objects.get(code='about')
  page, _ = Page.objects.get_or_create(code='about')
  return render(request, 'about.html', locals())


def contacts(request):
  # page = Page.objects.get(code='contacts')
  page, _ = Page.objects.get_or_create(code='contacts')
  return render(request, 'contacts.html', locals())



from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import path
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from shop.item.models import Item, ItemCategory
from .models import Page, PageFeature
from blog.models import Post, PostCategory, PostView
from shop.order.models import Order 
from project.utils import get_user 
from shop.cart.utils import get_cart, get_cart_info
from shop.cart.models import CartItem 


def index(request):
  # page = Page.objects.get(code='index')
  page, _ = Page.objects.get_or_create(code='index')
  top_items = Item.objects.all()[0:3]
  top_blog_categories = PostCategory.objects.all()[0:3]
  return render(request, 'index.html', locals())


def about(request):
  # page = Page.objects.get(code='about')
  page, _ = Page.objects.get_or_create(code='about')
  return render(request, 'about.html', locals())


def services(request):
  # page = Page.objects.get(code='services')
  page, _ = Page.objects.get_or_create(code='services')
  return render(request, 'services.html', locals())


def contacts(request):
  # page = Page.objects.get(code='contacts')
  page, _ = Page.objects.get_or_create(code='contacts')
  return render(request, 'contacts.html', locals())


def thank_you(request):
  # page = Page.objects.get(code='thank_you')
  page, _ = Page.objects.get_or_create(code='thank_you')
  return render(request, 'thank_you.html', locals())






def basket(request):
  # page = Page.objects.get(code='basket')
  page, _ = Page.objects.get_or_create(code='basket')
  cart = get_cart(request)
  cart_items = CartItem.objects.filter(ordered=False, cart=cart)
  total_price = 0 
  for cart_item in cart_items:
    total_price += cart_item.total_price * cart_item.quantity

  
  return render(request, 'shop/basket.html', locals())


def item_category(request, slug):
  category = get_object_or_404(ItemCategory, slug=slug)
  page = category
  if category.parent is None:
    return render(request, 'shop/items_list_main_category.html', locals())
  return render(request, 'shop/items_list.html', locals())


def item(request, slug):
  item = get_object_or_404(Item, slug=slug)
  page = item 
  return render(request, 'shop/item_detail.html', locals())


def search(request):
  # page = Page.objects.get(code='search')
  page, _ = Page.objects.get_or_create(code='search')
  return render(request, 'shop/search.html', locals())









def blog(request):
  # page = Page.objects.get(code='blog')
  page, _ = Page.objects.get_or_create(code='blog')
  post_categories = PostCategory.objects.all()
  return render(request, 'blog/category_list.html', locals())


def post(request, slug):
  post = Post.objects.get(slug=slug)
  page = post
  PostView.objects.get_or_create(
    sk=request.session.session_key,
    post=post
  )
  return render(request, 'blog/post_detail.html', locals())


def post_category(request, slug):
  post_category = get_object_or_404(PostCategory, slug=slug)
  posts = Post.objects.filter(category=post_category)
  page = post_category
  return render(request, 'blog/posts_list.html', locals())









@login_required
def profile(request):
  # page = Page.objects.get(code='profile')
  page, _ = Page.objects.get_or_create(code='profile')
  orders = Order.objects.filter(
    user=get_user(request),
    ordered=True,
  ).order_by('-id')
  print(orders.exists)
  return render(request, 'profile.html', locals())





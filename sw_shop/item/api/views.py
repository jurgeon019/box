from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.views.decorators.cache import cache_page
from box.sw_shop.item import settings as item_settings


from box.sw_shop.item.models import Item, ItemCategory, ItemReview
from box.sw_shop.item.api.serializers import ItemSerializer, ItemReviewSerializer
from box.sw_shop.cart.utils import get_cart
from box.core.utils import get_line
from box.sw_shop.item.api.search import filter_search
from box.core.mail import box_send_mail
from box.global_config.models import NotificationConfig, CatalogueConfig


def get_items_in_favours(request, items):
  items_in_favours = []
  for item in items:
    cart = get_cart(request)
    # if cart.favour_items.all().exists():
    if cart.favour_items.filter(item=item).exists():
      items_in_favours.append(item.id)
  return items_in_favours


def get_items_in_cart(request, items):
  items_in_cart = []
  for item in items:
    cart = get_cart(request)
    # if cart.cart_items.all().exists():
    if cart.items.filter(item=item).exists():
      items_in_cart.append(item.id)
  return items_in_cart





def filter_category(items, query):
  category = query.get('category')
  if category:
    if item_settings.MULTIPLE_CATEGORY:
      cat1 = ItemCategory.objects.all().get(slug=category)
      cat2 = ItemCategory.objects.all().filter(parent__slug=category)
      categories = [
        cat1,
      ]
      for cat in cat2:
        categories.append(cat)
      items = Item.active_objects.all().filter(categories__in=categories)
    else:
      items = items.filter(
        Q(category__slug=category) |
        Q(category__parent__slug=category) |
        Q(category__parent__parent__slug=category)
      ).distinct()
  return items



def paginate(items, query):
  page_number  = query.get('page', 1)
  per_page     = query.get('per_page', CatalogueConfig.get_solo().items_per_page)
  ordering     = query.get('sort', '-created')
  if not item_settings.PAGINATE_AJAX:
    page = items      
  else:
    page = Paginator(items, per_page=per_page).get_page(page_number)
    is_paginated = page.has_other_pages()
    current_page = page.number
    last_page    = page.paginator.num_pages
    page_range   = page.paginator.page_range
    has_prev     = page.has_previous()
    has_next     = page.has_next()
    next_url     = f'?page={page.next_page_number()}' if has_next else ''
    prev_url     = f'?page={page.previous_page_number()}' if has_prev else ''
    first_url    = f'?page=1'
    last_url     = f'?page={last_page}'
    response.update({
      'is_paginated':    is_paginated,
      'current_page':    current_page,
      'page_range':      list(page_range),
      'last_page':       last_page,
      'first_url':       first_url,
      'next_url':        next_url,
      'prev_url':        prev_url,
      'last_url':        last_url,
      'has_prev':        has_prev,
      'has_next':        has_next,
    })

  page_items = ItemSerializer(page, many=True, read_only=True).data
  response = {
    'paginated_items': page_items,
  }
  return response


def make_ordering(items, query):
  ordering = query.get('sort', '-created')
  if ordering:
    items = items.order_by(ordering)
  return items

@csrf_exempt
def get_items(request):
  query = request.POST
  items = Item.active_objects.all()
  items = filter_search(items, query)
  items = filter_category(items, query)
  items = make_ordering(items, query)
  response = paginate(items, query)

  # items_in_favours = get_items_in_favours(request, items)
  # items_in_cart    = get_items_in_cart(request, items)
  # json_items   = ItemSerializer(items, many=True, read_only=True).data
  # TODO: кешування. Коли на сайті 1000+ товарів, то вони серіалізуються 10 сеукнд
  response.update({
    # 'items_in_favours':items_in_favours,
    # 'items_in_cart':   items_in_cart,
    # 'json_items':      json_items,
  })
  return JsonResponse(response)


@csrf_exempt
def create_review(request):
    item_id = request.POST['item_id']
    text    = request.POST['text']
    phone   = request.POST['phone']
    name    = request.POST['name']
    rating  = request.POST['product_rating']
    item    = Item.objects.get(id=item_id)
    review  = ItemReview.objects.create(
      item=item,
      text=text,
      phone=phone,
      name=name,
      rating=rating,
    )
    if NotificationConfig.get_solo().auto_review_approval:
      review.is_active = True 
      review.save()
    json_review = ItemReviewSerializer(review).data
    response = {
      "review":json_review,
      "reviews_count":item.reviews.all().count(),
      "current_star":rating,
      "rounded_stars":item.rounded_stars,
      "stars":item.stars,
      "is_active":review.is_active,
    }
    box_send_mail(
      subject=NotificationConfig.get_colo().get_data('review')['subject'],
      recipient_list=NotificationConfig.get_colo().get_data('review')['emails'],
      model=review,
    )
    return JsonResponse(response)


@csrf_exempt
def get_item(request):
  query = request.POST
  query = request.GET
  item_id = query.get('item_id', 1)
  # item = Item.objects.get(id=item_id)
  item = Item.objects.get(id=item_id)
  item = ItemSerializer(item).data
  response = item
  return JsonResponse(response)


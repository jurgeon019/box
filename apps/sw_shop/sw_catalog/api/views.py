from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.views.decorators.cache import cache_page
from box.apps.sw_shop.sw_catalog import settings as item_settings


from box.apps.sw_shop.sw_catalog.models import Item, ItemCategory, ItemReview
from box.apps.sw_shop.sw_catalog.api.serializers import ItemDetailSerializer, ItemReviewSerializer
from box.apps.sw_shop.sw_cart.utils import get_cart
from box.core.utils import get_line
from box.apps.sw_shop.sw_catalog.api.search import filter_search
from box.core.mail import box_send_mail
from box.core.sw_global_config.models import GlobalConfig
from box.apps.sw_shop.sw_catalog.models import CatalogueConfig


from rest_framework import generics 
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import * 
from .paginators import * 


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


class ItemList(generics.ListCreateAPIView):
  queryset = Item.objects.all()
  serializer_class = ItemListSerializer
  pagination_class = StandardPageNumberPagination
  
  def list(self, request, *args, **kwargs):
    queryset = self.filter_queryset(self.get_queryset())

    page = self.paginate_queryset(queryset)
    if page is not None:
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    serializer = self.get_serializer(queryset, many=True)
    return Response(serializer.data)

  def get_queryset(self):
    '''
    :category_ids: айді категорІЙ(МАССИВ З ЦИФРАМИ)
    :max_price: максимальна ціна(цифра)
    :min_price: мінімальна ціна(цифра)
    :is_discount: true|false
    :ordering: -new_price | new_price 
    :attributes: 
    '''
    queryset     = super().get_queryset()
    data         = self.request.query_params
    category_id  = data.get('category_id', None)
    category_ids = data.get('category_ids', None)
    max_price    = data.get('max_price', None)
    min_price    = data.get('min_price', None)
    is_discount  = data.get('is_discount', None)
    ordering     = data.get('ordering', None)
    attributes   = data.get('attributes', [])
    # TODO: добавити сюда пошук по modelsearch,  get_items_in_favours, get_items_in_cart

    if category_id is not None:
      queryset = queryset.filter(category__id=category_id)
    if category_ids is not None:
      print(category_ids)
      print(type(category_ids))
      queryset = queryset.filter(category__id__in=[category_ids])
    if max_price is not None:
      queryset = queryset.filter(new_price__lte=max_price)
    if min_price is not None:
      queryset = queryset.filter(new_price__gte=min_price)
    # if is_discount is not None:
    if is_discount == 'true' or is_discount is True:
      # TODO: після переробки валют і цін глянути сюда
      # queryset = queryset.exclude(old_price__isnull=False)
      queryset = queryset.exclude(
        Q(discount__isnull=True) | 
        Q(old_price__isnull=True)
      ).distinct()
    if ordering is not None:
      queryset = queryset.order_by(ordering)
    for attribute in attributes:
      # глобальний атрибут, у якої було вибрано якісь значення
      attribute = Attribute.objects.get(id=attribute['attribute_id'])
      # вибрані значення у глобального атрибута(attribute)
      values = AttributeValue.objects.filter(id__in=attribute['value_ids'])
      # атрибути товарів у яких глобальний атрибут - вибраний атрибут(attribute)
      item_attributes = ItemAttribute.objects.filter(attribute=attribute)
      # значення атрибутів товарів у яких глобальни
      item_attribute_values = ItemAttributeValue.objects.filter(
        item_attribute__in=item_attributes,
        value__in=values,
      )
      item_attribute_value_ids = item_attribute_values.values_list('item_attribute', flat=True)
      item_ids = ItemAttribute.objects.filter(
        id__in=item_attribute_value_ids,
      ).values_list('item', flat=True)
      queryset = queryset.filter(id__in=item_ids)
    return queryset



class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Item.objects.all()
  serializer_class = ItemDetailSerializer
  pagination_class = StandardPageNumberPagination



class ReviewViewSet(ModelViewSet):
  queryset = ItemReview.objects.all().filter(is_active=True)
  serializer_class = ItemReviewSerializer











# OLD 





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
  response     = {}
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

  page_items = ItemDetailSerializer(page, many=True, read_only=True).data
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
  # json_items   = ItemDetailSerializer(items, many=True, read_only=True).data
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
    if GlobalConfig.get_solo().auto_review_approval:
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
      subject=GlobalConfig.get_colo().get_data('review')['subject'],
      recipient_list=GlobalConfig.get_colo().get_data('review')['emails'],
      model=review,
    )
    return JsonResponse(response)


@csrf_exempt
def get_item(request):
  query   = request.POST or request.GET
  item_id = query.get('item_id', 1)
  item = Item.objects.get(id=item_id)
  item = ItemDetailSerializer(item).data
  response = item
  return JsonResponse(response)



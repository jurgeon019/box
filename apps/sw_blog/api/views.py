from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt

from ..models import *
from .serializers import PostSerializer

from box.core.mail import box_send_mail
from box.core.sw_global_config.models import GlobalConfig
from box.apps.sw_shop.sw_catalog.models import CatalogueConfig

def filter_search(posts, query):
    search = query.get('q')
    if search:
        search = search.lower()
        print(search)
        print(posts.filter(title__icontains=search))
        posts = posts.filter(
            Q(title__icontains=search) | 
            Q(content__icontains=search)
        ).distinct()
    return posts 


def filter_category(posts, query):
    category = query.get('category')
    if category:
        posts = posts.filter(category__slug=category)
    return posts 


def paginate(posts, query):
    page_number  = query.get('page_number')
    per_page     = query.get('per_page', CatalogueConfig.get_solo().posts_per_page)
    page         = Paginator(posts, per_page=per_page).get_page(page_number)
    page_posts   = PostSerializer(page, many=True, read_only=True).data
    is_paginated = page.has_other_pages()
    current_page = page.number
    last_page    = page.paginator.num_pages
    pages_list   = page.paginator.page_range
    has_prev     = page.has_previous()
    has_next     = page.has_next()
    next_page    = page.next_page_number() if has_next else ''
    prev_page    = page.previous_page_number() if has_prev else ''
    response     = {
        'page_posts':   page_posts,
        'is_paginated': is_paginated,
        'current_page': current_page,
        'last_page':    last_page,
        'pages_list':   list(pages_list),
        'has_prev':     has_prev,
        'has_next':     has_next,
        'next_page':    next_page,
        'prev_page':    prev_page,
    }
    return response 


@csrf_exempt
def get_posts(request):
    query        = request.POST or request.GET
    posts        = Post.active_objects.all()
    posts        = filter_search(posts, query)
    posts        = filter_category(posts, query)
    response     = paginate(posts, query)
    # all_posts    = PostSerializer(posts, many=True, read_only=True).data
    # response.update({
    #     'all_posts':all_posts, 
    # })
    return JsonResponse(response)


@csrf_exempt
def search_posts(request):
    query = request.POST
    query = request.GET
    posts = Post.active_objects.all()
    posts = filter_search(posts, query)
    posts = filter_category(posts, query)
    posts = PostSerializer(posts, many=True).data
    response = {
        "posts":posts
    }
    return JsonResponse(response)



@csrf_exempt
def create_comment(request):
    # TODO: фукнція не дороблена.
    config = GlobalConfig.get_solo()
    query   = request.POST or request.GET
    post_id = query.get('post_id')
    text    = query.get('text')
    comment = PostComment.objects.create(
        text=text
    )
    if post_id:
        comment.post = Post.objects.get(id=post_id)
        comment.save()
    if config.auto_comment_approval:
        comment.is_active = True 
        comment.save()
    data = config.get_data('comment')
    box_send_mail(
        subject=data['subject'],
        recipients_list=data['emails'],
    )
    box_send_mail(
      subject      = f'Отримано коментар до блогу',
      template     = 'sw_blog/mail.html', 
      email_config = BlogRecipientEmail, 
      model        = comment,
    )


    response = {
        'status':'OK',
        'is_active':comment.is_active,
    }
    return JsonResponse(response)



from django.shortcuts import render 
from django import forms 
from django.http import HttpResponse 


def shop(request):
    categories       = ItemCategory.objects.all()
    main_categories  = ItemCategory.objects.filter(parent=None)
    items            = Item.objects.all()
    return render(request, 'test_shop/shop.html', locals())


def item(request, slug):
    item = Item.objects.get(slug=slug)
    x = reverse("item_category", kwargs={"slug": item.slug})
    print(x)
    return render(request, 'test_shop/item.html', locals())


def category(request, slug):
    categories       = ItemCategory.objects.all()
    main_categories  = ItemCategory.objects.filter(parent=None)
    category         = ItemCategory.objects.get(slug=slug)
    items            = Item.objects.all().filter(category=category)
    current_category = category
    return render(request, 'test_shop/category.html', locals())


def order(request):
    # form = OrderForm(request.POST or None)
    return render(request, 'test_shop/order.html', locals())



def mail(request):
    send_order_mail()
    return HttpResponse('sdfsdf')
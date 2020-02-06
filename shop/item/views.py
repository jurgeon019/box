
from django.shortcuts import render 
from box.shop.item.utils import read_items_from_xlsx_admin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages



@staff_member_required
def feed_items(request):
  if request.method == 'POST':
    f = request.FILES['file'] 
    read_items_from_xlsx_admin(f)
    messages.success(request, 'Товари були успішно завантажені')
  return render(request, 'feed_items.html', locals())




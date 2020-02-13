
from django.shortcuts import render 
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect 
from django.conf import settings 

from zipfile import ZipFile, ZIP_DEFLATED
from wsgiref.util import FileWrapper
import os 

from box.shop.item.utils import read_items_from_xlsx
from box.shop.item.models import Item


@staff_member_required
def feed_items(request):
  if request.method == 'POST':
    f = request.FILES['file'] 
    status = read_items_from_xlsx(f)
    if status:
      messages.success(request, 'Товари були успішно завантажені')
    else:
      messages.danger(reqeust, 'Сталась помилка')
  return render(request, 'feed_items.html', locals())


def export_item(request, slug=None):
  item = Item.objects.get(slug=slug)
  print()
  response = HttpResponse(FileWrapper(open('export.zip', 'rb')), content_type='application/zip')
  response['Content-Disposition'] = 'attachment; filename=items.csv'
  return response


def export_item_photoes(request, slug=None):
  # https://thispointer.com/python-how-to-create-a-zip-archive-from-multiple-files-or-directory/
  item   = Item.objects.get(slug=slug)
  images = item.images.all()
  # with ZipFile('export.zip', 'w') as export_zip:
  with ZipFile('export.zip', 'w', ZIP_DEFLATED) as export_zip:
    # image = images.first()
    # image_path = settings.MEDIA_ROOT+ image.image.url[6:]
    # image_name = image_path.split('/')[-1]
    # export_zip.write(image_path, image_name)
    # or 
    try:
      for image in images:
        filename = settings.MEDIA_ROOT + image.image.url[6:]
        arcname = os.path.join('shop', 'item', image.item.slug, filename.split('/')[-1])
        export_zip.write(
          filename=filename, 
          arcname=arcname,
        )
        # export_zip.write(filename, arcname)
    except: 
      pass
    # for root, dirs, files in os.walk(settings.MEDIA_ROOT):
    #   # print(root)
    #   # print(dirs)
    #   print()
    #   for f in files:
    #     # print("f: ", f)
    #     print()
    #     # export_zip.write(os.path.join(root, f))
  response = HttpResponse(FileWrapper(open('export.zip', 'rb')), content_type='application/zip')
  response['Content-Disposition'] = 'attachment; filename=export.zip'
  return response


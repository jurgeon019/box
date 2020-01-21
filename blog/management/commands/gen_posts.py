from django.core.management.base import BaseCommand
from box.blog.models import (
  Post, PostCategory
)
import random
import datetime 
import json 
import csv





class Command(BaseCommand):
  def handle(self, *args, **kwargs):
    amount = PostCategory.objects.all().count()
    last_item = Post.objects.all().last()
    if last_item:
      i = last_item.id + 1
    else:
      i = 0
    while True:
      i+=1
      m = f"post_{i}"
      post, _ = Post.objects.get_or_create(
        slug=m,
        title=m,
        content=m,
        category=PostCategory.objects.get(id=random.randint(1, amount))
      )
      print(post)
    self.stdout.write(self.style.SUCCESS('Data imported successfully'))


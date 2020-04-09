from django.core.management.base import BaseCommand
from box.apps.sw_blog.models import (
  Post, PostCategory
)
import random
import datetime 
import json 
import csv





class Command(BaseCommand):
  def handle(self, *args, **kwargs):
    amount = PostCategory.objects.all().count() or 1
    last_item = Post.objects.all().last()
    if last_item:
      i = last_item.id + 1
    else:
      i = 0
    while True:
      i+=1
      title   = f"Корпорація Kubota презентувала нові трактори серії М{i}"
      content = f"Трактор M511{i} потужністю 115 к.с. оснащений 4-циліндровим дизельним двигуном Kubota, який відповідає вимогам стандарту Euro IV."
      post, _ = Post.objects.get_or_create(
        title=title,
        content=content,
      )
      try:
        post.category=PostCategory.objects.get(id=random.randint(1, amount))
      except:
        pass
      post.save()
      print(post)
    self.stdout.write(self.style.SUCCESS('Data imported successfully'))


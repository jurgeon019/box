from tinymce.models import HTMLField
from django.db import models 
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone 
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.conf import settings 

from box.core.models import AbstractPage, BaseMixin

User = get_user_model() 



class Post(AbstractPage):
  content    = HTMLField(verbose_name=_("Контент"), blank=False, null=True)
  category   = models.ForeignKey(verbose_name=_("Категорія"), to="sw_blog.PostCategory", blank=True, null=True, on_delete=models.CASCADE)
  author     = models.ForeignKey(verbose_name=_("Автор"), to=User, on_delete=models.CASCADE, blank=True, null=True)
  # recomended = models.ManyToManyField(verbose_name=_("Рекомендовані товари"), to="sw_item.Item", blank=True, null=True)

  def save(self, *args, **kwargs):
    # print(self.recomended.all())
    # print(self.recomended.all().count())
    # TODO: при збереженні в рекомендованих товарах появляються всі товари
    if not self.slug:
      if self.title:
        title = slugify(self.title)
        self.slug = f"{title}"
    super().save(*args, **kwargs)

  class Meta:
    verbose_name = ('Публікація')
    verbose_name_plural = ('Публікації')
    ordering = ['order']

  def get_absolute_url(self):
      return reverse("post", kwargs={"slug": self.slug})


class PostCategory(AbstractPage):

  class Meta:
    verbose_name = ('Категорія')
    verbose_name_plural = ('Категорії')
    ordering = ['order']

  def get_absolute_url(self):
      return reverse("post_category", kwargs={"slug": self.slug})


class PostComment(BaseMixin):
  parent  = models.ForeignKey(to='self', on_delete=models.CASCADE, blank=True, null=True, related_name='subcomments')
  post    = models.ForeignKey(to="sw_blog.Post", blank=True, null=True, related_name='comments', on_delete=models.CASCADE)
  title   = models.CharField(verbose_name=_("Заголовок"),max_length=120, blank=True, null=True)
  content = models.TextField(verbose_name=_("Коммент"), blank=True, null=True)  
  author  = models.ForeignKey(verbose_name=_("Автор"), to=User,related_name='post_comments', on_delete=models.CASCADE, blank=True, null=True)
  
  def __str__(self):
    return f"{self.title}"

  class Meta:
    verbose_name = _('Коментар')
    verbose_name_plural = _('Коментарі')
    ordering = ['order']


class PostView(models.Model):
  sk   = models.CharField(max_length=255, blank=False, null=False)
  post = models.ForeignKey(to="sw_blog.Post", on_delete=models.CASCADE, related_name='views')

  def __str__(self):
    return f"{self.sk}:{self.post.id}"

  class Meta:
    verbose_name = _('Перегляд')
    verbose_name_plural = _('Перегляди')


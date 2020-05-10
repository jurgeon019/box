from tinymce.models import HTMLField
# from froala_editor.fields import FroalaField
# from markdownx.models import MarkdownxField
# from django_markdown.models import MarkdownField
# from markdownx.models import MarkdownxField
# from ckeditor.fields import RichTextField
# from ckeditor_uploader.fields import RichTextUploadingField
# from djangocms_text_ckeditor.fields import HTMLField


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
  markers    = models.ManyToManyField(
    to="sw_global_config.GlobalMarker", verbose_name=_("Маркери"), blank=True
  )
  # content = RichTextUploadingField(
  # content = RichTextField(
    # config_name='awesome_ckeditor',
  # content = models.TextField(
  # content = MarkdownxField(
  # content = MarkdownField(
  content    = HTMLField(
  # content = FroalaField(
    # options={
    #   'toolbarInline': False,
    # },
    # plugins=('font_size', 'font_family'),
    verbose_name=_("Контент"), blank=False, null=True)
  category   = models.ForeignKey(
    verbose_name=_("Категорія"), to="sw_blog.PostCategory", 
    blank=True, null=True, on_delete=models.CASCADE,
  )
  author     = models.ForeignKey(
    verbose_name=_("Автор"), to=User, on_delete=models.CASCADE, 
    blank=True, null=True,
  )

  def save(self, *args, **kwargs):
    if not self.slug:
      if self.title:
        title = slugify(self.title)
        self.slug = f"{title}"
    super().save(*args, **kwargs)

  class Meta:
    verbose_name = _('Публікація')
    verbose_name_plural = _('Публікації')
    ordering = [
      '-order'
    ]

  def get_absolute_url(self):
      return reverse("post", kwargs={"slug": self.slug})


class PostCategory(AbstractPage):

  class Meta:
    verbose_name = _('Категорія')
    verbose_name_plural = _('Категорії')
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


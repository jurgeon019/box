from django.db import models 
# try:
#   from tinymce.models import HTMLField
# except:
#   from tinymce import HTMLField

from tinymce.models import HTMLField
# from tinymce import HTMLField

# from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model() 


class Post(models.Model):
  meta_title = models.TextField(verbose_name="Мета Заголовок",        blank=True, null=True)
  meta_descr = models.TextField(verbose_name="Мета Опис",             blank=True, null=True)
  meta_key   = models.TextField(verbose_name="Мета ключові слова",    blank=True, null=True)
  slug       = models.SlugField(verbose_name="Посилання на публікацію", blank=False, null=False, max_length=255, unique=True)
  title      = models.CharField(verbose_name=("Заголовок публікації"),blank=True, null=True, max_length=120,)
  # content    = RichTextField(verbose_name=("Контент"), blank=True, null=True)  
  # content    = RichTextUploadingField(verbose_name=("Контент"), blank=True, null=True)  
  content    = HTMLField(verbose_name="Контент", blank=True, null=True)
  category   = models.ForeignKey(verbose_name=("Категорія"), to="blog.PostCategory", blank=True, null=True, on_delete=models.CASCADE)
  author     = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
  image      = models.ImageField(verbose_name="Картинка", blank=True, null=True, default='blog/test_blog.png')
  alt        = models.CharField(verbose_name=("Альт до картинки"), max_length=255, blank=True, null=True)
  updated    = models.DateTimeField(verbose_name="Оновлено", auto_now_add=False, auto_now=True, blank=True, null=True)
  created    = models.DateTimeField(verbose_name="Створено", auto_now_add=True,  auto_now=False, blank=True, null=True)
  
  @property
  def views_count(self):
    views = self.views.all().count()
    # print(views)
    return views
    return '123'

  def __str__(self):
    return f'{self.title}'

  class Meta:
    verbose_name = 'Публікація'
    verbose_name_plural = 'Публікації'

  def get_absolute_url(self):
      return reverse("post", kwargs={"slug": self.slug})


class PostCategory(models.Model):
  meta_title  = models.TextField(verbose_name=("Мета Заголовок"),      blank=True, null=True)
  meta_descr  = models.TextField(verbose_name=("Мета Опис"),           blank=True, null=True)
  meta_key    = models.TextField(verbose_name=("Мета Ключові слова"),  blank=True, null=True)
  title       = models.TextField(verbose_name=("Заголовок"),           blank=True, null=True)
  description = models.TextField(verbose_name=("Опис категорії"),      blank=True, null=True)
  slug        = models.SlugField(verbose_name=("Посилання"), unique=True, blank=False,null=False, max_length=255, )
  image       = models.ImageField(verbose_name=("Картинка категорії"), blank=True, null=True, default='blog/test_blog.png')
  alt         = models.CharField(verbose_name=("Альт до картинки"), max_length=120,    blank=True, null=True)
  updated     = models.DateTimeField(verbose_name="Оновлено", auto_now_add=False, auto_now=True, blank=True, null=True)
  created     = models.DateTimeField(verbose_name="Створено", auto_now_add=True,  auto_now=False, blank=True, null=True)

  def __str__(self):
    return f'{self.title}'

  class Meta:
    verbose_name = 'Категорія'
    verbose_name_plural = 'Категорії'

  def get_absolute_url(self):
      return reverse("post_category", kwargs={"slug": self.slug})


class PostComment(models.Model):
  parent  = models.ForeignKey(to='self', on_delete=models.CASCADE, blank=True, null=True, related_name='subcomments')
  post    = models.ForeignKey(to="blog.Post", blank=True, null=True, related_name='comments', on_delete=models.CASCADE)
  title   = models.CharField(verbose_name=("Заголовок"),max_length=120, blank=True, null=True)
  content = models.TextField(verbose_name=("Коммент"), blank=True, null=True)  
  author  = models.ForeignKey(verbose_name=("Автор"), to=User,related_name='post_comments', on_delete=models.CASCADE, blank=True, null=True)
  updated = models.DateTimeField(verbose_name="Оновлено", auto_now_add=False, auto_now=True, blank=True, null=True)
  created = models.DateTimeField(verbose_name="Створено", auto_now_add=True, auto_now=False, blank=True, null=True)

  def __str__(self):
    return f"{self.title}"

  class Meta:
    verbose_name = 'Коментар'
    verbose_name_plural = 'Коментарі'


class PostView(models.Model):
  sk   = models.CharField(max_length=120, blank=True, null=True)
  post = models.ForeignKey(to="blog.Post", on_delete=models.CASCADE, related_name='views')
  def __str__(self):
    return f"{self.title}"

  class Meta:
    verbose_name = 'Перегляд'
    verbose_name_plural = 'Перегляди'




# from django.db.models.signals import post_save 
# from blog.tasks import simple_task
 

 
# def user_post_save(sender, instance, signal, *args, **kwargs):
#   print("user_post_save")
#   # Post.objects.create(slug=instance.slug+'sdf')
#   simple_task.delay()

# post_save.connect(user_post_save, sender=Post)
from django.utils.translation import gettext_lazy as _

from ._imports import * 
from .currency import ItemCurrency



# class ItemCategory(AbstractPage, MPTTModel):
  # parent     = TreeForeignKey(verbose_name=_("Батьківська категорія"), to='self', blank=True, null=True, on_delete=models.SET_NULL, related_name='subcategories')
class ItemCategory(AbstractPage):
  parent     = models.ForeignKey(verbose_name=_("Батьківська категорія"), to='self', blank=True, null=True, on_delete=models.SET_NULL, related_name='subcategories')

  currency   = models.ForeignKey(verbose_name=_("Валюта"), to="item.ItemCurrency", blank=True, null=True, related_name="categories",  on_delete=models.SET_NULL)
  # TODO: визначити якого хуя з включеним ActiveManager дочірні категорії(subcategories) виводяться не ті шо треба, а всі підряд

  class Meta: 
    verbose_name = _('категорія'); 
    verbose_name_plural = _('категорії'); 
    unique_together = ('title', 'parent')
    ordering = ['order']
  
  def get_absolute_url(self):
    return 
    return reverse("item_category", kwargs={"slug": self.slug})

  @property
  def parent_slug(self):
    slug = ''
    if self.parent: slug = self.parent.slug	
    return slug
  
  @property
  def parents(self):
    parent = self.parent 
    parents = [self, parent]
    # parents = [parent]
    if parent:
      while parent.parent:
        parent = parent.parent 
        parents.append(parent)
        # parents.insert(0, parent)
    # parents = reversed(parents)
    return parents[-1::-1]

  @property
  def tree_title(self):
    parents = self.get_ancestors(ascending=False, include_self=False)
    parents = list(parents.values_list('title', flat=True))
    # parents += self.title
    parents.append(self.title)
    result  = ' -> '.join(parents)
    # result = self.title
    # try:
    # 	full_path = [self.title]      
    # 	parent = self.parent
    # 	while parent is not None:
    # 		print(parent)
    # 		full_path.append(parent.title)
    # 		parent = parent.parent
    # 	result = ' -> '.join(full_path[::-1]) 
    # except Exception as e:
    # 	print(e)
    # 	result = self.title
    return result

  def __str__(self):     
    result = f'{self.tree_title}'
    if self.currency:
      result += f' ({self.currency})'
    return result

  def save(self, *args, **kwargs):

    if self.currency:
      # try:
      # 	self.items.all().update(currency=self.currency)
      # except:
      # 	pass
      pass

    elif not self.currency:
      alls  = ItemCurrency.objects.all()
      mains = alls.filter(is_main=True)
      if mains.exists():
        self.currency = mains.first()
      elif alls.exists():
        self.currency = alls.first()


    title = self.title.lower().strip()
    # origin_title = title
    # numb = 1
    # while ItemCategory.objects.filter(title=title).exists():
    # 	title = f'{origin_title} ({numb})'
    # 	numb += 1
    self.title = title
    if not self.slug:
      try:
        slug = slugify(translit(self.title, reversed=True), allow_unicode=True) 
      except Exception as e:
        slug = slugify(translit(self.title, 'uk', reversed=True), allow_unicode=True) 
      except Exception as e:
        slug = slugify(translit(self.title, 'ru', reversed=True), allow_unicode=True) 
      except Exception as e:
        slug = slugify(self.title, allow_unicode=True)
      if slug == '':
        slug = slugify(self.title, allow_unicode=True)

      # numb = 1
      # origin_slug = slug 
      # while ItemCategory.objects.filter(slug=slug).exists():
      # 	slug = f'{origin_slug}-{numb}'
      # 	numb += 1



      self.slug  = slug
      cats = ItemCategory.objects.filter(slug=slug)
      # if cats.exists():
      # 	cat = cats.first()
      # print(slug)
      # print(cat)

    super().save(*args, **kwargs)

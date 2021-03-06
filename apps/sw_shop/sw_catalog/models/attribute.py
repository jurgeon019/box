from django.db import models 
from django.utils.translation import gettext_lazy as _
from box.core.sw_currency.models import Currency


class AttributeCategory(models.Model):
    name   = models.CharField(
        verbose_name=_("Назва"), max_length=255, unique=True
    )
    def __str__(self):
        return f'{self.name}'
    
    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.lower().strip()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('категорія атрибутів')
        verbose_name_plural = _('категорії атрибутів')

    @classmethod
    def modeltranslation_fields(cls):
        return ['name']


class Attribute(models.Model):
    code = models.SlugField(
        verbose_name=_("Код"), max_length=255, unique=True, blank=True, null=True
    )
    name = models.CharField(
        verbose_name=_("Назва"), max_length=50, unique=True, 
    )
    category = models.ForeignKey(
        verbose_name=_("Категорія"), to="sw_catalog.AttributeCategory", 
        related_name="attributes", on_delete=models.SET_NULL, 
        blank=True, null=True,
    )

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.lower().strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('атрибут')
        verbose_name_plural = _('атрибути')
        unique_together = [
            'name',
            'category',
        ]

    def get_attribute_values(self, items=None):
        item_attributes = ItemAttribute.objects.all()
        if items: item_attributes = item_attributes.filter(item__in=items)
        item_attribute_value_ids = ItemAttributeValue.objects.filter(
            item_attribute__in=item_attributes.filter(attribute=self),
        ).values_list('value_id', flat=True).distinct()
        return AttributeValue.objects.filter(id__in=item_attribute_value_ids) 

    @classmethod
    def modeltranslation_fields(cls):
        return ['name']


class AttributeValue(models.Model):
    code = models.SlugField(
        verbose_name=_("Код"), max_length=255, unique=True, 
        blank=True, null=True,
    )
    attribute = models.ForeignKey(
        verbose_name=_("Атрибут"), to="sw_catalog.Attribute", 
        # on_delete=models.CASCADE, 
        on_delete=models.SET_NULL, 
        # blank=True, 
        null=True,
    )
    value = models.CharField(
        verbose_name=_("Значення"), max_length=255, unique=True,
    )

    def __str__(self):
        return f'{self.value}'
    
    def save(self, *args, **kwargs):
        if self.value:
            self.value = self.value.lower().strip()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('значення атрибуту')
        verbose_name_plural = _('значення атрибутів')

    @classmethod
    def modeltranslation_fields(cls):
        return ['value']




class ItemAttributeValue(models.Model):
    item_attribute = models.ForeignKey(
        to="sw_catalog.ItemAttribute", verbose_name=_("Атрибут товару"), on_delete=models.CASCADE,
        related_name='variants',
    )
    value = models.ForeignKey(
        verbose_name=_("Значення"), 
        to='sw_catalog.AttributeValue', 
        on_delete=models.CASCADE,
    )
    price = models.DecimalField(
        verbose_name=_("Ціна"), max_digits=9, decimal_places=2, default=0,
    )
    currency = models.ForeignKey(
        verbose_name=_("Валюта"), to="sw_currency.Currency", 
        on_delete=models.CASCADE, blank=True, null=True
    )
    amount = models.PositiveIntegerField(
		verbose_name=_("Кількість"), blank=True, null=True, default=None,
		help_text=_('0 - товар з таким значенням характеристики відсутній. Порожнє поле - необмежена кількість.'),
	)
    description = models.TextField(
        verbose_name=_("Опис"), blank=True, null=True, 
    )

    # TODO: виводити тільки ті характеристики товару у яких amount > 0 
    # TODO: відмінусовувати amount у характеристики товару при заказі 
    # TODO: виводити тільки ті характеристики товару у яких is_active=True

    def save(self, *args, **kwargs):
      if not self.currency:
        self.currency = Currency.objects.get(is_main=True)
      super().save(*args, **kwargs)

    @classmethod
    def modeltranslation_fields(self):
        return ['description',]

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = _('значення атрибутів товарів')
        verbose_name_plural = _('значення атрибутів товарів')
        unique_together = [
            'item_attribute',
            'value',
        ]





class ItemAttribute(models.Model):
    item = models.ForeignKey(
        verbose_name=_("Товар"), to="sw_catalog.Item", 
        on_delete=models.CASCADE, related_name='item_attributes',
    )
    attribute = models.ForeignKey(
        verbose_name=_("Атрибут"), to='sw_catalog.Attribute', 
        on_delete=models.CASCADE,
    )
    is_option = models.BooleanField(
        verbose_name=_("Опція?"), default=False
    )
   
    def get_values(self):
        return ItemAttributeValue.objects.filter(item_attribute=self)

    @property
    def has_multiple_values(self):
        return self.values.all().count() > 1


    def __str__(self):
        try:
            return f'{self.attribute.name}'
        except:
            return f'{self.id}'

    class Meta:
        verbose_name = _("атрибут товару")
        verbose_name_plural = _("атрибути товарів")
        unique_together = [
            'item',
            'attribute',
        ]

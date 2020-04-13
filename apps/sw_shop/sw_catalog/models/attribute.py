from django.db import models 
from django.utils.translation import gettext_lazy as _


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
    name = models.CharField(
        verbose_name=_("Назва"), max_length=50, 
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
    
    @classmethod
    def modeltranslation_fields(cls):
        return ['name']


class AttributeVariantValue(models.Model):
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
        verbose_name = _('значення варіантів атрибутів')
        verbose_name_plural = _('значення варіантів атрибутів')

    @classmethod
    def modeltranslation_fields(cls):
        return ['value']


class AttributeVariant(models.Model):
    value = models.ForeignKey(
        verbose_name=_("Значення"), 
        to='sw_catalog.AttributeVariantValue', 
        on_delete=models.CASCADE,
        # unique=True,
    )
    price = models.DecimalField(
        verbose_name=_("Ціна"), max_digits=9, decimal_places=2, default=0,
    )
    description = models.TextField(
        verbose_name=_("Опис"), blank=True, null=True, 
    )

    @classmethod
    def modeltranslation_fields(self):
        return ['description',]

    def __str__(self):
        return f'{self.value}'

    class Meta:
        abstract = True 


class ObjAttribute(models.Model):
    is_option = models.BooleanField(
        verbose_name=_("Опція?"), default=False
    )
    attribute = models.ForeignKey(
        verbose_name=_("Атрибут"), to='sw_catalog.Attribute', 
        on_delete=models.CASCADE,
    )

    @property
    def has_multiple_values(self):
        return self.values.all().count() > 1

    def __str__(self):
        return f'{self.attribute.name}'

    class Meta:
        abstract = True 


# Item 


class ItemAttribute(ObjAttribute):
    item = models.ForeignKey(
        verbose_name=_("Товар"), to="sw_catalog.Item", 
        on_delete=models.CASCADE, related_name='item_attributes',
    )

    class Meta:
        verbose_name = _("атрибут товарів")
        verbose_name_plural = _("атрибути товарів")
        unique_together = [
            'item',
            'attribute',
        ]


class ItemAttributeVariant(AttributeVariant):
    item_attribute = models.ForeignKey(
        to="sw_catalog.ItemAttribute", verbose_name=_("Атрибут товару"), on_delete=models.CASCADE,
        related_name='variants',
    )

    class Meta:
        verbose_name = _('варіант значення атрибуту товару')
        verbose_name_plural = _('варіанти значеннь атрибутів товару')





# Item Category 

class ItemCategoryAttribute(ObjAttribute):
    # item_category = models.ForeignKey(
    #     verbose_name=_("Категорія"), to="sw_catalog.ItemCategory", 
    #     on_delete=models.CASCADE, related_name='item_category_attributes',
    # )
    item_categories = models.ManyToManyField(
        verbose_name=_("Категорія"), 
        to="sw_catalog.ItemCategory", 
        related_name='item_category_attributes',
    )
    variants = models.ManyToManyField(
        verbose_name=_("Варіанти атрибутів товарів"), 
        to="sw_catalog.ItemCategoryAttributeVariant", 
        related_name='item_category_attributes',
    )
    class Meta:
        verbose_name = _("атрибут категорій товарів")
        verbose_name_plural = _("атрибути категорій товарів")


class ItemCategoryAttributeVariant(AttributeVariant):
    class Meta:
        verbose_name = _('варіант атрибутів категорій товарів')
        verbose_name_plural = _('варіанти атрибутів категорій товарів')







'''
AttributeCategory
    name = charfield 

Attribute
    name     = charfield 
    category = fk to AttributeCategory

AttributeVariantValue
    value = textfield

ItemAttribute(ObjAttribute)
    item       = fk to Item 
    *is_option = boolean*
    *attribute = fk to Attribute*

ItemAttributeVariant(AttributeVariant)
    item_attribute = fk to ItemAttribute
    *value         = fk to AttributeVariantValue*
    *price         = decimalfield*
    *description   = textfield*




ObjAttribute __abstract__ 
    is_option = boolean
    attribute = fk to Attribute

AttributeVariant __abstract__ 
    value       = fk to AttributeVariantValue
    price       = decimalfield
    description = textfield
'''
from django.db import models 

from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.utils.translation import gettext_lazy as _


class Category(MPTTModel):
    parent  = TreeForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    title   = models.CharField(max_length=255)
    code    = models.SlugField(blank=True, null=True, unique=True)
    def __str__(self):
        return self.title


class Item(models.Model):
    category = TreeForeignKey(Category, on_delete=models.CASCADE)
    title    = models.CharField(max_length=255)

    def __str__(self):
        return self.title


# Variants


class ItemVariant(models.Model):
    item = models.ForeignKey('sw_dev.Item', on_delete=models.CASCADE)


# Options 


class ItemOption(models.Model):
    product = models.ForeignKey("sw_dev.Item",             on_delete=models.CASCADE)
    name    = models.ForeignKey('sw_dev.ItemOptionName',  on_delete=models.CASCADE)
    price   = models.DecimalField(max_digits=9, decimal_places=7)
    help_text = models.TextField()

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        unique_together = ['name', 'product']


class ItemOptionName(models.Model):
    name    = models.CharField(max_length=255)



# Features


class ItemFeature(models.Model):
    product = models.ForeignKey("sw_dev.Item",             on_delete=models.CASCADE)
    name    = models.ForeignKey('sw_dev.ItemFeatureName',  on_delete=models.CASCADE)
    value   = models.ForeignKey('sw_dev.ItemFeatureValue', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'


class ItemFeatureValue(models.Model):
    value     = models.CharField(max_length=50)
    price     = models.DecimalField(max_digits=9, decimal_places=7)
    help_text = models.TextField()

    def __str__(self):
        return f'{self.name}'


class ItemFeatureName(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'


# Attriburtes


class ItemAttribute(models.Model):
    def __str__(self):
        return f'{self.name}'
    product = models.ForeignKey("sw_dev.Item", verbose_name=_(""), on_delete=models.CASCADE)
    name = models.ForeignKey(to='sw_dev.ItemAttributeName', on_delete=models.CASCADE)


class ItemAttributeName(models.Model):
    def __str__(self):
        return f'{self.name}'
    name = models.CharField(max_length=50)


class ItemAttributeValue(models.Model):
    attribute = models.ForeignKey("sw_dev.ItemAttribute", verbose_name=_(""), on_delete=models.CASCADE)
    # value = models.CharField(max_length=50)
    value = models.ForeignKey('sw_dev.ItemAttributeValueValue', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9, decimal_places=7)
    help_text = models.TextField()

    def __str__(self):
        return f'{self.value}'


class ItemAttributeValueValue(models.Model):
    def __str__(self):
        return f'{self.value}'
    value = models.CharField(max_length=50)
    code  = models.SlugField()
    price = models.DecimalField(max_digits=9, decimal_places=7)
    help_text = models.TextField()





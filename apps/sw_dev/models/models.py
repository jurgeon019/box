

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



class Product(models.Model):
    category = TreeForeignKey(Category, on_delete=models.CASCADE)
    title    = models.CharField(max_length=255)

    def __str__(self):
        return self.title





class ProductAttribute(models.Model):
    def __str__(self):
        return f'{self.name}'
    product = models.ForeignKey("dev.Product", verbose_name=_(""), on_delete=models.CASCADE)
    name = models.ForeignKey(to='dev.ProductAttributeName', max_length=50, on_delete=models.CASCADE)


class ProductAttributeName(models.Model):
    def __str__(self):
        return f'{self.name}'
    name = models.CharField(_("name"), max_length=50)



class ProductAttributeValue(models.Model):
    def __str__(self):
        return f'{self.value}'
    attribute = models.ForeignKey("dev.ProductAttribute", verbose_name=_(""), on_delete=models.CASCADE)
    # value = models.CharField(_("Value"), max_length=50)
    value = models.ForeignKey('dev.ProductAttributeValueValue', on_delete=models.CASCADE)


class ProductAttributeValueValue(models.Model):
    def __str__(self):
        return f'{self.value}'
    value = models.CharField(_("Value"), max_length=50)




# from django.conf import settings 


# class Item(models.Model):
#    name = models.CharField('name', max_length=164)


# class Attr(models.Model):
#    name = models.CharField('name', max_length=164)
#    item = models.ForeignKey(Item, on_delete=models.CASCADE,)


# class Value(models.Model):
#    name = models.CharField('name', max_length=164)
#    attr = models.ForeignKey(Attr, on_delete=models.CASCADE,)



# from django.contrib import admin
# from nested_admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline
# from .models import *


# class ValueInline(NestedTabularInline):
#    model = Value
#    extra = 1


# class AttrInline(NestedStackedInline):
#    model = Attr
#    extra = 1
#    inlines = [
#        ValueInline, 
#     ]


# class ItemAdmin(NestedModelAdmin):
#    inlines = [
#        AttrInline,
#     ]


# admin.site.register(Item, ItemAdmin)


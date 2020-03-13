from django.db import models 
from django.shortcuts import reverse 
from adminsortable.models import SortableMixin

class Faq(SortableMixin):
    name      = models.CharField(verbose_name=("Назва"), max_length=255)
    answer    = models.TextField(verbose_name=("Відповідь"))
    is_active = models.BooleanField(verbose_name=("Активність"), default=True)
    order = models.PositiveIntegerField(verbose_name=("Порядок"), default=0, editable=False, db_index=True)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = ("FAQ")
        verbose_name_plural = ("FAQ")
        ordering = ['order']
    
    def get_absolute_url(self):
        return reverse("faq", kwargs={"pk": self.pk})
    
    @classmethod
    def modeltranslation_fields(cls):        
        fields = [
            'name',
            'answer',
        ]
        return fields

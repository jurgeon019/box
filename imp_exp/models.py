from django.db import models 


class ImportLog(models.Model):
    item   = models.ForeignKey(verbose_name=("Товаp"), related_name='import_logs', to='item.Item', on_delete=models.CASCADE)
    status = models.CharField(verbose_name=("Статус"), max_length=255)
    def __str__(self):
        return f'{self.item}' 
    class Meta:
        verbose_name        = 'Журнал імпорту'
        verbose_name_plural = 'Журнал імпорту'




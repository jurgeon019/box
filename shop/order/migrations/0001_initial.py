# Generated by Django 3.0.3 on 2020-02-24 15:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('item', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=24, null=True, verbose_name='Статус')),
            ],
            options={
                'verbose_name': 'Статус замовлення',
                'verbose_name_plural': 'Статуси замовлення',
            },
        ),
        migrations.CreateModel(
            name='OrderRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name="Ім'я")),
                ('surname', models.CharField(blank=True, max_length=255, null=True, verbose_name='Фамілія')),
                ('phone', models.CharField(blank=True, max_length=255, null=True, verbose_name='Телефон')),
                ('email', models.CharField(blank=True, max_length=255, null=True, verbose_name='Емайл')),
                ('created', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Створено')),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='item.Item', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Покупка в один клік',
                'verbose_name_plural': 'покупки в 1 клік',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Сумма замовлення')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Імя')),
                ('email', models.CharField(blank=True, max_length=255, null=True, verbose_name='Е-майл')),
                ('phone', models.CharField(blank=True, max_length=255, null=True, verbose_name='Номер телефона')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Адрес')),
                ('comments', models.TextField(blank=True, default=None, null=True, verbose_name='Коментарии')),
                ('payment_opt', models.CharField(blank=True, help_text=' ', max_length=255, null=True, verbose_name='Спосіб оплати')),
                ('delivery_opt', models.CharField(blank=True, max_length=255, null=True, verbose_name='Спосіб доставки')),
                ('ordered', models.BooleanField(default=False, verbose_name='Завершений')),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата створення')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Дата обовлення')),
                ('status', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='order.Status', verbose_name='Статус')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='Користувач')),
            ],
            options={
                'verbose_name': 'Замовлення товарів',
                'verbose_name_plural': 'Замовлення товарів',
            },
        ),
    ]

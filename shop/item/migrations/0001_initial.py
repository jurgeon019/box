# Generated by Django 3.0.3 on 2020-02-24 15:00

import box.shop.item.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Назва валюти')),
                ('is_main', models.BooleanField(default=False, help_text='Якщо валюта головна, то відносно неї будуть конвертуватись інші валюти на сайті', verbose_name='Головна')),
            ],
            options={
                'verbose_name': 'Валюта',
                'verbose_name_plural': 'Валюти',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meta_title', models.TextField(blank=True, null=True, verbose_name='Мета заголовок')),
                ('meta_title_uk', models.TextField(blank=True, null=True, verbose_name='Мета заголовок')),
                ('meta_title_ru', models.TextField(blank=True, null=True, verbose_name='Мета заголовок')),
                ('meta_descr', models.TextField(blank=True, null=True, verbose_name='Мета опис')),
                ('meta_descr_uk', models.TextField(blank=True, null=True, verbose_name='Мета опис')),
                ('meta_descr_ru', models.TextField(blank=True, null=True, verbose_name='Мета опис')),
                ('meta_key', models.TextField(blank=True, null=True, verbose_name='Мета ключові слова')),
                ('meta_key_uk', models.TextField(blank=True, null=True, verbose_name='Мета ключові слова')),
                ('meta_key_ru', models.TextField(blank=True, null=True, verbose_name='Мета ключові слова')),
                ('title', models.CharField(max_length=255, verbose_name='Назва')),
                ('title_uk', models.CharField(max_length=255, null=True, verbose_name='Назва')),
                ('title_ru', models.CharField(max_length=255, null=True, verbose_name='Назва')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Опис')),
                ('description_uk', models.TextField(blank=True, null=True, verbose_name='Опис')),
                ('description_ru', models.TextField(blank=True, null=True, verbose_name='Опис')),
                ('code', models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='Артикул')),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, unique=True, verbose_name='Ссилка')),
                ('thumbnail', models.ImageField(blank=True, upload_to='shop/items/thumbnails', verbose_name='Маленька картинка')),
                ('old_price', models.FloatField(blank=True, null=True, verbose_name='Стара ціна')),
                ('new_price', models.FloatField(blank=True, null=True, verbose_name='Актуальна ціна')),
                ('amount', models.IntegerField(blank=True, default=1, null=True, verbose_name='Кількість')),
                ('is_active', models.BooleanField(default=True, help_text='Присутність товару на сайті в списку товарів', verbose_name='Активний')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Створений')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Оновлений')),
                ('order', models.IntegerField(default=10, verbose_name='Порядок')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товари',
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='ItemFeatureName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Назва характеристики')),
            ],
            options={
                'verbose_name': 'назва характеристики',
                'verbose_name_plural': 'назви характеристики',
            },
        ),
        migrations.CreateModel(
            name='ItemManufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Назва')),
            ],
            options={
                'verbose_name': 'Виробник',
                'verbose_name_plural': 'Виробники',
            },
        ),
        migrations.CreateModel(
            name='ItemMarker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255, unique=True, verbose_name='Код')),
                ('text', models.CharField(max_length=255, verbose_name='Текст')),
            ],
            options={
                'verbose_name': 'Маркер',
                'verbose_name_plural': 'Маркери',
            },
        ),
        migrations.CreateModel(
            name='ItemStock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255, unique=True, verbose_name='Наявність')),
            ],
            options={
                'verbose_name': 'Наявність',
                'verbose_name_plural': 'Наявність',
            },
        ),
        migrations.CreateModel(
            name='ItemReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=255, null=True, verbose_name='Відгук')),
                ('phone', models.CharField(blank=True, max_length=255, null=True, verbose_name='Телефон')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name="Ім'я")),
                ('rating', models.CharField(blank=True, max_length=255, null=True, verbose_name='Оцінка')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='item.Item', verbose_name='Товар')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Відгук',
                'verbose_name_plural': 'Відгуки',
            },
        ),
        migrations.CreateModel(
            name='ItemImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, default='shop/items/test_item.jpg', null=True, upload_to=box.shop.item.models.item_image_folder, verbose_name='Ссилка зображення')),
                ('alt', models.CharField(blank=True, max_length=255, null=True, verbose_name='Альт')),
                ('alt_uk', models.CharField(blank=True, max_length=255, null=True, verbose_name='Альт')),
                ('alt_ru', models.CharField(blank=True, max_length=255, null=True, verbose_name='Альт')),
                ('order', models.IntegerField(default=1, verbose_name='Порядок')),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='item.Item', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Зображення товару',
                'verbose_name_plural': 'Зображення товару',
            },
        ),
        migrations.CreateModel(
            name='ItemFeatureCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='Назва категорії')),
                ('name_uk', models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='Назва категорії')),
                ('name_ru', models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='Назва категорії')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='item.ItemFeatureCategory', verbose_name='Батьківська категорія')),
            ],
            options={
                'verbose_name': 'Категорія характеристики',
                'verbose_name_plural': 'Категорії характеристики',
            },
        ),
        migrations.CreateModel(
            name='ItemFeature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Назва характеристики')),
                ('name_uk', models.CharField(blank=True, max_length=255, null=True, verbose_name='Назва характеристики')),
                ('name_ru', models.CharField(blank=True, max_length=255, null=True, verbose_name='Назва характеристики')),
                ('code', models.CharField(blank=True, max_length=255, null=True, verbose_name='Код')),
                ('value', models.TextField(blank=True, null=True, verbose_name='Значення характеристики')),
                ('value_uk', models.TextField(blank=True, null=True, verbose_name='Значення характеристики')),
                ('value_ru', models.TextField(blank=True, null=True, verbose_name='Значення характеристики')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='item.ItemFeatureCategory', verbose_name='Категорія характеристики')),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='features', to='item.Item', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Характеристика товару',
                'verbose_name_plural': 'Характеристики товару',
            },
        ),
        migrations.CreateModel(
            name='ItemCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meta_title', models.TextField(blank=True, null=True, verbose_name='Мета заголовок')),
                ('meta_title_uk', models.TextField(blank=True, null=True, verbose_name='Мета заголовок')),
                ('meta_title_ru', models.TextField(blank=True, null=True, verbose_name='Мета заголовок')),
                ('meta_descr', models.TextField(blank=True, null=True, verbose_name='Мета опис')),
                ('meta_descr_uk', models.TextField(blank=True, null=True, verbose_name='Мета опис')),
                ('meta_descr_ru', models.TextField(blank=True, null=True, verbose_name='Мета опис')),
                ('meta_key', models.TextField(blank=True, null=True, verbose_name='Мета ключові слова')),
                ('meta_key_uk', models.TextField(blank=True, null=True, verbose_name='Мета ключові слова')),
                ('meta_key_ru', models.TextField(blank=True, null=True, verbose_name='Мета ключові слова')),
                ('slug', models.SlugField(max_length=255, null=True, unique=True, verbose_name='Посилання')),
                ('code', models.CharField(blank=True, help_text='Код для прогера', max_length=255, null=True, verbose_name='Код')),
                ('title', models.CharField(max_length=255, verbose_name='Назва')),
                ('title_uk', models.CharField(max_length=255, null=True, verbose_name='Назва')),
                ('title_ru', models.CharField(max_length=255, null=True, verbose_name='Назва')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='shop/category', verbose_name='Картинка')),
                ('alt', models.CharField(blank=True, max_length=255, null=True, verbose_name='Альт до картинки')),
                ('is_active', models.BooleanField(default=True, help_text='Присутність категорії на сайті', verbose_name='Чи активна')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Створено')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Оновлено')),
                ('currency', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='item.Currency', verbose_name='Валюта')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='item.ItemCategory', verbose_name='Батьківська категорія')),
            ],
            options={
                'verbose_name': 'категорія',
                'verbose_name_plural': 'категорії',
            },
        ),
        migrations.AddField(
            model_name='item',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='items', to='item.ItemCategory', verbose_name='Категорія'),
        ),
        migrations.AddField(
            model_name='item',
            name='currency',
            field=models.ForeignKey(blank=True, help_text='Якщо залишити порожнім, то буде встановлена валюта категорії, у якій знаходиться товар', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='items', to='item.Currency', verbose_name='Валюта'),
        ),
        migrations.AddField(
            model_name='item',
            name='in_stock',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='item.ItemStock'),
        ),
        migrations.AddField(
            model_name='item',
            name='manufacturer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='items', to='item.ItemManufacturer', verbose_name='Виробник'),
        ),
        migrations.AddField(
            model_name='item',
            name='markers',
            field=models.ManyToManyField(related_name='items', to='item.ItemMarker', verbose_name='Маркери'),
        ),
        migrations.CreateModel(
            name='CurrencyRatio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ratio', models.FloatField(help_text='Скільки одиниць порівнюваної валюти міститься в 1 одиниці головної валюти', verbose_name='Співвідношення')),
                ('compared', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratio_compared', to='item.Currency', verbose_name='Порівнювана валюта')),
                ('main', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratio_main', to='item.Currency', verbose_name='Головна валюта')),
            ],
            options={
                'verbose_name': 'Співвідношення валют',
                'verbose_name_plural': 'Співвідношення валют',
                'unique_together': {('main', 'compared')},
            },
        ),
    ]

# Generated by Django 3.0.3 on 2020-02-18 20:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=30, null=True, unique=True, verbose_name='Код')),
                ('meta_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Заголовок')),
                ('meta_descr', models.TextField(blank=True, null=True, verbose_name='Опис')),
                ('meta_key', models.TextField(blank=True, null=True, verbose_name='Ключові слова')),
                ('url', models.CharField(blank=True, max_length=255, null=True, verbose_name='Урл')),
            ],
            options={
                'verbose_name': 'Сторінка',
                'verbose_name_plural': 'Сторінки',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='PageImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, help_text='Код, по якому картинка буде діставатися у хтмл-шаблоні', max_length=120, null=True, verbose_name='Код')),
                ('name', models.CharField(blank=True, help_text='Допоміжна назва, яка буде нагадувати де знаходиться картинка', max_length=120, null=True, verbose_name='Назва')),
                ('value', models.ImageField(blank=True, help_text='Картинка, яка буде відображатися на сайті', null=True, upload_to='pages/', verbose_name='Картинка')),
                ('page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='pages.Page', verbose_name='Сторінка')),
            ],
            options={
                'verbose_name': 'Картинки на сторінці',
                'verbose_name_plural': 'Картинки на сторінці',
                'unique_together': {('page', 'code')},
            },
        ),
        migrations.CreateModel(
            name='PageFeature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, help_text='Код, по якому контент буде діставатися у хтмл-шаблоні', max_length=120, null=True, verbose_name='Код')),
                ('name', models.CharField(blank=True, help_text='Допоміжна назва, яка буде нагадувати де на сторінці знаходиться текст', max_length=120, null=True, verbose_name='Назва')),
                ('value', models.TextField(blank=True, help_text='Контент, який буде відображатися на сайті', null=True, verbose_name='Текст')),
                ('page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='features', to='pages.Page', verbose_name='Сторінка')),
            ],
            options={
                'verbose_name': 'текст сторінки',
                'verbose_name_plural': 'Текста сторінки',
                'unique_together': {('page', 'code')},
            },
        ),
    ]

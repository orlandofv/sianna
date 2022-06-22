# Generated by Django 3.2.12 on 2022-06-22 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('isis', '0042_alter_product_warehouse'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, default='/media/default.jpg', upload_to='media', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='gallery',
            name='image',
            field=models.ImageField(default='/media/default.jpg', upload_to='media', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='/media/default.jpg', upload_to='media', verbose_name='Primary Image'),
        ),
    ]
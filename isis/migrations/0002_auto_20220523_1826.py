# Generated by Django 3.2.12 on 2022-05-23 18:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('isis', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Wharehouse',
            new_name='Warehouse',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='phisical_stock',
            new_name='physical_stock',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='purchace_status',
            new_name='purchase_status',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='wharehouse',
            new_name='warehouse',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='weight_measurement',
            new_name='weight_measurements',
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='default.jpg', upload_to='media', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='product',
            name='images',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='isis.gallery'),
        ),
    ]

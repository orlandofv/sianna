# Generated by Django 3.2.12 on 2022-05-25 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('isis', '0014_rename_parent_warehouse_warehouse_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='type',
            field=models.CharField(choices=[('SERVICE', 'Service'), ('PRODUCT', 'Product')], default='PRODUCT', max_length=10, verbose_name='Type'),
        ),
    ]

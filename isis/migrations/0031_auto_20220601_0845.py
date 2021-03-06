# Generated by Django 3.2.12 on 2022-06-01 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0004_alter_supplierinvoice_warehouse'),
        ('warehouse', '0001_initial'),
        ('isis', '0030_stockmovement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='warehouse',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='warehouse.warehouse'),
        ),
        migrations.AlterField(
            model_name='product',
            name='warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='warehouse.warehouse', verbose_name='Default Warehouse'),
        ),
        migrations.AlterField(
            model_name='stockmovement',
            name='warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='warehouse.warehouse'),
        ),
        migrations.DeleteModel(
            name='Warehouse',
        ),
    ]

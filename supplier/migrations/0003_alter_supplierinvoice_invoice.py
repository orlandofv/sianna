# Generated by Django 3.2.12 on 2022-05-31 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0002_supplierinvoice_invoice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplierinvoice',
            name='invoice',
            field=models.CharField(help_text='Supplier Invoice Number(Ex: Invoice: 12345)', max_length=100, verbose_name='Invoice Number'),
        ),
    ]

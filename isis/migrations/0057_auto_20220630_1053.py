# Generated by Django 3.2.12 on 2022-06-30 10:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('isis', '0056_auto_20220630_0835'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='receiptinvoice',
            options={'verbose_name': 'Receipt Invoice', 'verbose_name_plural': 'Receipt Invoices'},
        ),
        migrations.AlterField(
            model_name='invoice',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 30, 10, 53, 14, 920025), verbose_name='Due Date'),
        ),
        migrations.AlterUniqueTogether(
            name='receiptinvoice',
            unique_together=set(),
        ),
    ]
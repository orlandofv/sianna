# Generated by Django 3.2.12 on 2022-07-04 13:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('isis', '0073_auto_20220704_1358'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoicing',
            name='document',
        ),
        migrations.AlterField(
            model_name='invoice',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 3, 13, 59, 50, 278178), verbose_name='Due Date'),
        ),
        migrations.AlterField(
            model_name='invoicing',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 3, 13, 59, 50, 268143), verbose_name='Due Date'),
        ),
    ]

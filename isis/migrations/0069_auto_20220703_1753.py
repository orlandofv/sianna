# Generated by Django 3.2.12 on 2022-07-03 17:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('isis', '0068_auto_20220703_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 2, 17, 53, 51, 337539), verbose_name='Due Date'),
        ),
        migrations.AlterField(
            model_name='invoicing',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 2, 17, 53, 51, 337539), verbose_name='Due Date'),
        ),
    ]

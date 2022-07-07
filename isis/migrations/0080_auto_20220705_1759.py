# Generated by Django 3.2.12 on 2022-07-05 17:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('isis', '0079_auto_20220705_1755'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentmethod',
            name='active_status',
            field=models.IntegerField(choices=[(1, 'Active'), (0, 'Deactivated')], default=1),
        ),
        migrations.AddField(
            model_name='paymentterm',
            name='active_status',
            field=models.IntegerField(choices=[(1, 'Active'), (0, 'Deactivated')], default=1),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 4, 17, 59, 13, 90140), verbose_name='Due Date'),
        ),
        migrations.AlterField(
            model_name='invoicing',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 4, 17, 59, 13, 83105), verbose_name='Due Date'),
        ),
    ]
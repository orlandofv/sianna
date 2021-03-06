# Generated by Django 3.2.12 on 2022-07-03 11:33

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('isis', '0061_auto_20220703_1130'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Documents',
            new_name='Document',
        ),
        migrations.AlterField(
            model_name='invoice',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 2, 11, 33, 7, 573412), verbose_name='Due Date'),
        ),
        migrations.AlterField(
            model_name='invoicing',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 2, 11, 33, 7, 563317), verbose_name='Due Date'),
        ),
    ]

# Generated by Django 3.2.12 on 2022-06-29 21:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_alter_user_last_active_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_active_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 6, 29, 21, 16, 52, 861455), verbose_name='Last Active Date'),
        ),
    ]

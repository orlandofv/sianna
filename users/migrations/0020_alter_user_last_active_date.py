# Generated by Django 3.2.12 on 2022-06-30 11:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_alter_user_last_active_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_active_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 6, 30, 11, 9, 9, 901738), verbose_name='Last Active Date'),
        ),
    ]

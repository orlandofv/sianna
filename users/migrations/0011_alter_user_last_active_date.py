# Generated by Django 3.2.12 on 2022-06-26 21:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_user_last_active_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_active_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 6, 26, 21, 33, 34, 429587), verbose_name='Last Active Date'),
        ),
    ]

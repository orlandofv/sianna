# Generated by Django 3.2.12 on 2022-07-03 17:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0029_alter_user_last_active_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_active_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 7, 3, 17, 50, 51, 880804), verbose_name='Last Active Date'),
        ),
    ]
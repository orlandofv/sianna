# Generated by Django 3.2.12 on 2022-05-11 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset_app', '0036_item_unity'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='parent',
            field=models.IntegerField(default=0, help_text='Choose Parent Company', verbose_name='Parent Company'),
        ),
    ]

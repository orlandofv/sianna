# Generated by Django 3.2.12 on 2022-04-16 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset_app', '0018_auto_20220416_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companysettings',
            name='address',
            field=models.TextField(blank=True, verbose_name='Address'),
        ),
    ]

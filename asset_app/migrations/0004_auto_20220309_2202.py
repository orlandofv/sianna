# Generated by Django 2.2.7 on 2022-03-09 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset_app', '0003_auto_20220309_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assets',
            name='status',
            field=models.IntegerField(choices=[(1, 'Good'), (0, 'Broken')], default=1),
        ),
    ]

# Generated by Django 3.2.12 on 2022-05-23 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('isis', '0008_auto_20220523_2237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tax',
            name='active_status',
            field=models.IntegerField(choices=[(1, 'Active'), (0, 'Deactivated')], default=1, verbose_name='Status'),
        ),
    ]
# Generated by Django 3.2.12 on 2022-05-28 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('isis', '0022_auto_20220528_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='active_status',
            field=models.IntegerField(default=1),
        ),
    ]

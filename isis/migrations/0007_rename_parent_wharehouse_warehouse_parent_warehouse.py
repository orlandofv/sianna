# Generated by Django 3.2.12 on 2022-05-23 22:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('isis', '0006_auto_20220523_2147'),
    ]

    operations = [
        migrations.RenameField(
            model_name='warehouse',
            old_name='parent_wharehouse',
            new_name='parent_warehouse',
        ),
    ]
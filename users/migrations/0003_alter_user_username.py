# Generated by Django 3.2.12 on 2022-06-23 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_delete_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=20, unique=True, verbose_name='Username'),
        ),
    ]

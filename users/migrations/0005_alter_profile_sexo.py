# Generated by Django 3.2.12 on 2022-04-18 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_first_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='sexo',
            field=models.IntegerField(choices=[(1, 'Male'), (2, 'Female')], default=1, help_text=False, verbose_name='Sexo'),
        ),
    ]
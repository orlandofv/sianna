# Generated by Django 2.2.7 on 2022-03-16 20:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asset_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='branch',
            options={'ordering': ('branch_name',), 'verbose_name_plural': 'Branches'},
        ),
        migrations.AlterModelOptions(
            name='company',
            options={'ordering': ('company_name',), 'verbose_name_plural': 'Companies'},
        ),
    ]

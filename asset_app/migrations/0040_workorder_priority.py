# Generated by Django 3.2.12 on 2022-05-12 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset_app', '0039_alter_company_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='workorder',
            name='priority',
            field=models.CharField(choices=[('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')], default='LOW', max_length=10, verbose_name='Priority'),
        ),
    ]

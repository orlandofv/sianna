# Generated by Django 3.2.12 on 2022-04-20 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset_app', '0033_alter_workorder_progress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allocation',
            name='allocation_no',
            field=models.PositiveIntegerField(unique=True, verbose_name='Allocation No.'),
        ),
        migrations.AlterField(
            model_name='component',
            name='component_no',
            field=models.PositiveIntegerField(unique=True, verbose_name='System no'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='frequency',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='order',
            field=models.PositiveIntegerField(unique=True, verbose_name='Order Number'),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='progress',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Work Progress (%)'),
        ),
    ]

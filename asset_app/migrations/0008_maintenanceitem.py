# Generated by Django 3.2.12 on 2022-04-07 21:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asset_app', '0007_remove_item_maintenance'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaintenanceItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Quantity')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asset_app.item')),
                ('maintenance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asset_app.maintenance')),
            ],
        ),
    ]

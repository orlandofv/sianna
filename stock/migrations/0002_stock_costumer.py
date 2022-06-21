# Generated by Django 3.2.12 on 2022-06-01 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asset_app', '0058_auto_20220531_2233'),
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='costumer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='asset_app.costumer'),
            preserve_default=False,
        ),
    ]
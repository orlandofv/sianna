# Generated by Django 3.2.12 on 2022-05-27 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset_app', '0050_auto_20220526_1618'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='costumer',
            options={'ordering': ('name',), 'verbose_name_plural': 'Costumers'},
        ),
        migrations.RemoveField(
            model_name='costumer',
            name='manager',
        ),
        migrations.AddField(
            model_name='costumer',
            name='is_supplier',
            field=models.IntegerField(choices=[(1, 'No'), ('1', 'Yes')], default=1),
        ),
        migrations.AddField(
            model_name='costumer',
            name='max_credit',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=18),
        ),
        migrations.AddField(
            model_name='costumer',
            name='website',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]
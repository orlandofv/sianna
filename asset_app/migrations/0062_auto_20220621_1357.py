# Generated by Django 3.2.12 on 2022-06-21 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset_app', '0061_alter_workorder_active_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='costumer',
            name='contacts',
        ),
        migrations.AddField(
            model_name='costumer',
            name='capital',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=18),
        ),
        migrations.AddField(
            model_name='costumer',
            name='city',
            field=models.CharField(blank=True, max_length=100, verbose_name='City'),
        ),
        migrations.AddField(
            model_name='costumer',
            name='country',
            field=models.CharField(blank=True, max_length=100, verbose_name='Country'),
        ),
        migrations.AddField(
            model_name='costumer',
            name='fax',
            field=models.CharField(blank=True, max_length=255, verbose_name='Fax'),
        ),
        migrations.AddField(
            model_name='costumer',
            name='mobile',
            field=models.CharField(blank=True, max_length=255, verbose_name='Mobile'),
        ),
        migrations.AddField(
            model_name='costumer',
            name='phone',
            field=models.CharField(blank=True, max_length=255, verbose_name='Phone'),
        ),
        migrations.AddField(
            model_name='costumer',
            name='province',
            field=models.CharField(blank=True, max_length=100, verbose_name='Province/State'),
        ),
        migrations.AddField(
            model_name='costumer',
            name='zip_code',
            field=models.CharField(blank=True, max_length=100, verbose_name='Zip Code'),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='active_status',
            field=models.IntegerField(choices=[(1, 'Active'), (0, 'Deactivated')], default=1, verbose_name='Active Status'),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='status',
            field=models.CharField(blank=True, choices=[('Pending', 'Pending'), ('InProgress', 'InProgress'), ('Finished', 'Finished'), ('Abandoned', 'Abandoned')], default='Pending', max_length=15, verbose_name='Progress'),
        ),
    ]

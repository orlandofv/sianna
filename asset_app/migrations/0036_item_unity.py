# Generated by Django 3.2.12 on 2022-05-11 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset_app', '0035_alter_workorder_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='unity',
            field=models.CharField(choices=[('Cm', 'Cm'), ('Kg', 'Kg'), ('Lt', 'Lt'), ('Gb', 'Gb'), ('Mb', 'Mb'), ('Piece', 'Piece'), ('M3', 'M3'), ('Km', 'Km'), ('G', 'G')], default='Piece', max_length=10, verbose_name='Unity'),
        ),
    ]

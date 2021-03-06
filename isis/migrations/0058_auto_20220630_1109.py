# Generated by Django 3.2.12 on 2022-06-30 11:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('isis', '0057_auto_20220630_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 30, 11, 9, 10, 27667), verbose_name='Due Date'),
        ),
        migrations.AlterUniqueTogether(
            name='receiptinvoice',
            unique_together={('receipt', 'invoice')},
        ),
    ]

# Generated by Django 3.2.12 on 2022-06-26 21:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('isis', '0048_auto_20220626_1036'),
    ]

    operations = [
        migrations.AddField(
            model_name='receiptinvoice',
            name='paid',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=18),
        ),
        migrations.AddField(
            model_name='receiptinvoice',
            name='total',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=18),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 26, 21, 33, 34, 518801), verbose_name='Due Date'),
        ),
        migrations.AlterUniqueTogether(
            name='receiptinvoice',
            unique_together={('invoice', 'receipt')},
        ),
    ]

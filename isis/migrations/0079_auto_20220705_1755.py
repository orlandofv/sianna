# Generated by Django 3.2.12 on 2022-07-05 17:55

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('isis', '0078_auto_20220704_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 4, 17, 55, 50, 435154), verbose_name='Due Date'),
        ),
        migrations.AlterField(
            model_name='invoicing',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 4, 17, 55, 50, 432147), verbose_name='Due Date'),
        ),
        migrations.CreateModel(
            name='DocumentPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=6, default=0, max_digits=18)),
                ('notes', models.CharField(blank=True, max_length=255)),
                ('file', models.ImageField(blank=True, default='/media/default.jpg', upload_to='media', verbose_name='Add File')),
                ('invoicing', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='isis.invoicing')),
                ('payment_method', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='isis.paymentmethod')),
            ],
        ),
    ]

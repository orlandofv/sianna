# Generated by Django 3.2.12 on 2022-07-03 11:30

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('asset_app', '0069_auto_20220622_0059'),
        ('warehouse', '0003_alter_userwarehouse_unique_together'),
        ('isis', '0060_alter_invoice_due_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='documents',
            name='track_due_date',
            field=models.IntegerField(choices=[(1, 'Yes'), (0, 'No')], default=0, verbose_name='Track Due Date?'),
        ),
        migrations.AddField(
            model_name='documents',
            name='track_payment',
            field=models.IntegerField(choices=[(1, 'Yes'), (0, 'No')], default=0, verbose_name='Track Payment?'),
        ),
        migrations.AlterField(
            model_name='documents',
            name='modify_stock',
            field=models.IntegerField(choices=[(1, 'Yes'), (0, 'No')], default=0, verbose_name='Modify Stock?'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 2, 11, 30, 15, 993550), verbose_name='Due Date'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='notes',
            field=models.TextField(blank=True, verbose_name='Private Notes'),
        ),
        migrations.CreateModel(
            name='Invoicing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('number', models.IntegerField(unique=True)),
                ('slug', models.SlugField(editable=False, unique=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date')),
                ('due_date', models.DateTimeField(default=datetime.datetime(2022, 8, 2, 11, 30, 15, 986569), verbose_name='Due Date')),
                ('credit', models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=18)),
                ('debit', models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=18)),
                ('total', models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=18)),
                ('total_tax', models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=18)),
                ('subtotal', models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=18)),
                ('total_discount', models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=18)),
                ('paid_status', models.IntegerField(default=0)),
                ('delivered_status', models.IntegerField(default=0)),
                ('finished_status', models.IntegerField(default=0)),
                ('active_status', models.IntegerField(default=1)),
                ('notes', models.TextField(blank=True, verbose_name='Private Notes')),
                ('public_notes', models.TextField(blank=True, verbose_name='Public Notes')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('costumer', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='asset_app.costumer', verbose_name='Costumer')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('payment_method', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='isis.paymentmethod')),
                ('payment_term', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='isis.paymentterm')),
                ('warehouse', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='warehouse.warehouse')),
            ],
            options={
                'ordering': ('-name',),
            },
        ),
    ]
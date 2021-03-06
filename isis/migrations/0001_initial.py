# Generated by Django 3.2.12 on 2022-05-18 20:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default.jpg', upload_to='media', verbose_name='Image')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Gallery',
                'ordering': ('-date_created',),
            },
        ),
        migrations.CreateModel(
            name='Wharehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('slug', models.SlugField(editable=False, unique=True)),
                ('parent_wharehouse', models.IntegerField(default=0)),
                ('description', models.TextField(blank=True)),
                ('address', models.TextField(blank=True)),
                ('contacts', models.CharField(blank=True, max_length=255)),
                ('active_status', models.IntegerField(choices=[(1, 'Active'), (0, 'Deactivated')], default=1)),
                ('open_status', models.CharField(choices=[('OPEN', 'Open'), ('CLOSE', 'Close')], default='OPEN', max_length=25)),
                ('notes', models.TextField(blank=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('slug', models.SlugField(editable=False, unique=True)),
                ('rate', models.DecimalField(decimal_places=2, default=0, max_digits=4)),
                ('active_status', models.IntegerField(choices=[(1, 'Active'), (0, 'Deactivated')], default=1)),
                ('notes', models.TextField(blank=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField(editable=False, unique=True)),
                ('parent_product', models.IntegerField(default=0)),
                ('description', models.TextField(blank=True)),
                ('barcode', models.CharField(blank=True, max_length=255)),
                ('sell_price', models.DecimalField(decimal_places=6, default=0, max_digits=18)),
                ('min_sell_price', models.DecimalField(decimal_places=6, default=0, max_digits=18)),
                ('sell_price2', models.DecimalField(decimal_places=6, default=0, max_digits=18)),
                ('sell_price3', models.DecimalField(decimal_places=6, default=0, max_digits=18)),
                ('sell_price4', models.DecimalField(decimal_places=6, default=0, max_digits=18)),
                ('sell_price5', models.DecimalField(decimal_places=6, default=0, max_digits=18)),
                ('purchase_price', models.DecimalField(decimal_places=6, default=0, max_digits=18)),
                ('phisical_stock', models.DecimalField(decimal_places=6, default=0, max_digits=18)),
                ('stock_limit', models.DecimalField(decimal_places=6, default=0, max_digits=18)),
                ('desired_stock', models.DecimalField(decimal_places=6, default=0, max_digits=18)),
                ('image', models.ImageField(default='default.jpg', upload_to='media', verbose_name='Image')),
                ('product_nature', models.CharField(choices=[('raw_product', 'Raw Product'), ('manufactured_product', 'Manufactured Product')], default='raw_product', max_length=50)),
                ('product_url', models.URLField(blank=True, max_length=255)),
                ('weight', models.DecimalField(decimal_places=6, default=0, max_digits=9)),
                ('length', models.DecimalField(decimal_places=6, default=0, max_digits=9)),
                ('width', models.DecimalField(decimal_places=6, default=0, max_digits=9)),
                ('height', models.DecimalField(decimal_places=6, default=0, max_digits=9)),
                ('length_measurements', models.CharField(choices=[('m', 'm'), ('dm', 'dm'), ('cm', 'cm'), ('mm', 'mm'), ('ft', 'ft'), ('in', 'in')], default='m', max_length=10)),
                ('area', models.DecimalField(decimal_places=6, default=0, max_digits=9)),
                ('area_measurements', models.CharField(choices=[('m2', 'm??'), ('dm2', 'dm??'), ('cm2', 'cm??'), ('mm2', 'mm??'), ('ft2', 'ft??'), ('in2', 'in??')], default='m2', max_length=10)),
                ('volume', models.DecimalField(decimal_places=6, default=0, max_digits=9)),
                ('volume_choices', models.CharField(choices=[('m3', 'm??'), ('dm3', 'dm??'), ('cm3', 'cm??'), ('mm3', 'mm??'), ('ft3', 'ft??'), ('in3', 'in??'), ('litre', 'litre'), ('gallon', 'gallon')], default=0, max_length=10)),
                ('weight_measurement', models.CharField(choices=[('kg', 'Kg'), ('g', 'G'), ('mg', 'MG'), ('ounce', 'ounce'), ('pound', 'pound'), ('ton', 'ton')], default='kg', max_length=50)),
                ('active_status', models.IntegerField(choices=[(1, 'Active'), (0, 'Deactivated')], default=1)),
                ('sell_status', models.IntegerField(choices=[(1, 'For Sale'), (0, 'Not for Sale')], default=1)),
                ('purchace_status', models.IntegerField(choices=[(1, 'For Purchase'), (0, 'Not for Purchase')], default=1)),
                ('notes', models.TextField(blank=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('images', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='isis.gallery')),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('tax', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='isis.tax')),
                ('wharehouse', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='isis.wharehouse')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
    ]

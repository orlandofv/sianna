# Generated by Django 3.2.12 on 2022-05-31 17:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('isis', '0029_auto_20220529_2019'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockMovement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.CharField(max_length=50)),
                ('quantity', models.DecimalField(decimal_places=6, default=0, max_digits=18)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='isis.product')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='isis.warehouse')),
            ],
            options={
                'ordering': ('-date_created',),
            },
        ),
    ]

# Generated by Django 4.1.5 on 2023-02-08 07:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sales_app', '0006_sales_invoice_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='sales',
            name='sales_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
# Generated by Django 5.1.4 on 2025-02-18 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_product_price_per_unit_product_weight'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, upload_to='category/%Y/%m/%d'),
        ),
    ]

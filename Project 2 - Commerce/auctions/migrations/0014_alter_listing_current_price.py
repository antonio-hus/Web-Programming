# Generated by Django 5.0.2 on 2024-03-01 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_listing_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='current_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
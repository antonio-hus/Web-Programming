# Generated by Django 5.0.2 on 2024-02-28 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_productcategory_alter_listing_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='photo',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]

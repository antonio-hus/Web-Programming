# Generated by Django 5.0.2 on 2024-02-15 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_listing_comment_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=3),
            preserve_default=False,
        ),
    ]
# Imports Section
from django.contrib.auth.models import AbstractUser
from django.db import models


# Defining the models
class User(AbstractUser):
    wishlist = models.ManyToManyField('Listing', blank=True, null=True)


class ProductCategory(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return self.category


class Listing(models.Model):
    """
    Every Auction should have:
    - * one owner
    - * one title
    - * one description
    - * one start price
    - * one current price
    - * one category
    - one photo
    """
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name="listings")
    photo = models.CharField(max_length=256, null=True, blank=True)

    start_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)


class Bid(models.Model):
    """
    Every Bid should have:
    - * one auction listing
    - * one owner
    - * one value
    """
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    bid = models.DecimalField(max_digits=10, decimal_places=2)


class Comment(models.Model):
    """
    Every Comment should have:
    - * one auction listing
    - * one owner
    - * one rating
    - * one title
    - * one description
    - one photo

    Restrictions - review value (0.0 - 5.0)
    """
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")

    rating = models.DecimalField(max_digits=3, decimal_places=1)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    # TODO: Add photo option for comment


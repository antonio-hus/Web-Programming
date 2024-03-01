# Imports Section
from django.contrib import admin
from .models import User, Listing, Bid, Comment, ProductCategory

# Admin Privileges over Models Below
# In real-world application - Remove User, and Bid Edit Privileges

# User Data
admin.site.register(User)

# Listings
admin.site.register(Listing)

# Bids
admin.site.register(Bid)

# Comments
admin.site.register(Comment)

# Categories
admin.site.register(ProductCategory)

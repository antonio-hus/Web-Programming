# Imports Section
from django.contrib import admin
from .models import User, Post, Comment, Like

# Registering models in the admin site
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)

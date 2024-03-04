from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Each User Shall Have:
    * ... Abstract User Fields,
    * Followers,
    * Followings
    """
    follower = models.ManyToManyField('self', related_name='followings', symmetrical=False)
    following = models.ManyToManyField('self', related_name='followers', symmetrical=False)


class Post(models.Model):
    """
    Each Post Shall Have:
    * one owner,
    * one body,
    * one timestamp of last edit
    """
    pass


class Like(models.Model):
    """
    Each Like Shall Have:
    * one owner,
    * one post on which it belongs
    """
    pass


class Comment(models.Model):
    """
    Each Comment Shall Have:
    * one owner,
    * one post on which it belongs
    """
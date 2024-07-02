# Imports Section
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    User Class:
    - inherits all fields of AbstractUser ( username, email, password, etc. )
    - adds ManyToMany relation - followers / following
    """
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following')

    def __str__(self):
        return self.username

    def get_followers(self):
        return self.followers.all()

    def get_following(self):
        return self.following.all()


class Post(models.Model):
    """
    Post Class:
    - has an owner ( User )
    - has a body ( Content )
    - has a timestamp ( Now )
    - has a ManyToMany relationship - likes
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    body = models.TextField(max_length=256)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, through='Like', related_name='liked_posts')

    def __str__(self):
        return f'{self.owner.username}: {self.body[:20]}...'


class Like(models.Model):
    """
    Like Class:
    - has an owner ( User )
    - has a post ( Post which was liked )
    - has a timestamp ( Now )
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="like_set")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.owner.username} likes {self.post.body[:20]}...'


class Comment(models.Model):
    """
    Comment Class:
    - has an owner ( User )
    - has a post ( Post which was commented )
    - has a body ( Content )
    - has a timestamp ( Now )
    """
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField(max_length=256)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.owner.username} commented on {self.post.body[:20]}: {self.body[:20]}...'

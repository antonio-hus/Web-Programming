from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.core import serializers

from .models import User, Post
from .forms import PostForm


def index(request):
    form = PostForm()
    return render(request, "network/index.html", {"form": form})


def following(request):
    form = PostForm()
    return render(request, "network/following.html", {"form": form})


def user(request, username: str):
    return render(request, "network/user.html", {"username": username})


################################
######## GETTER METHODS ########
################################

def get_posts(data):

    # JSON Serialized List
    posts_data = []

    # Parsing input data and formatting to JSON Format
    for post in data:
        post_dict = {
            'id': post.id,
            'body': post.body,
            'timestamp': post.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'owner': post.owner.username,
            'likesCount': post.likes.count()
        }
        posts_data.append(post_dict)

    # Returning data in JSON Serialized Format
    return posts_data


def get_all_posts(request):

    # Getting all posts from the database
    posts = Post.objects.all().order_by('timestamp')
    posts_data = get_posts(posts)

    # Returning data in JSON Format
    return JsonResponse(posts_data, safe=False)


def get_following_posts(request):

    # Getting all following user's posts from the database
    following = request.user.get_following()
    posts = Post.objects.filter(owner__in=following).order_by('timestamp')
    posts_data = get_posts(posts)

    # Returning data in JSON Format
    return JsonResponse(posts_data, safe=False)


def get_posts_by_user(id: int):

    # Getting the posts of the user with the given username
    posts = Post.objects.filter(owner=id).order_by('timestamp')
    posts_data = get_posts(posts)

    # Returning data in JSON Format
    return posts_data


def get_user(request, username: str):

    # Getting the user by its unique username
    user = User.objects.get(username=username)

    # Fetching the user's data
    user_data = {
        "username": username,
        "is_authenticated": request.user.is_authenticated,
        "is_owner": user.username == request.user.username,
        "is_following": user.followers.filter(id=request.user.id).exists(),
        "followerCount": user.followers.count(),
        "followingCount": user.following.count(),
        "posts": get_posts_by_user(user.id)
    }

    # Returning JSON Formatted Data
    return JsonResponse(user_data, safe=False)


################################
######## POST METHODS ##########
################################

def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            user = request.user
            content = form.cleaned_data['content']
            Post.objects.create(owner=user, body=content, timestamp=timezone.now())
            return HttpResponseRedirect(reverse("index"))

    else:
        return HttpResponseRedirect(reverse("index"))


def follow_user(request, username):
    if request.method == "POST":
        # Getting the user by username
        user = User.objects.get(username=username)

        # Checking if the current user is already following the user
        if user.followers.filter(id=request.user.id).exists():
            # Already a follower => Unfollow
            user.followers.remove(request.user)

        else:
            # Not already a follower => Follow
            user.followers.add(request.user)

        # Follow methods was successful
        return JsonResponse({"status": "success", "username": username})

    # Methods was not post, failed follow method
    return JsonResponse({"status": "failed"}, status=400)


################################
#### AUTHENTICATION METHODS ####
################################

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

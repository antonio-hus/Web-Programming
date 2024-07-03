# IMPORTS SECTION
# Framework Defined
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Python Packages
import json
# User Defined
from .models import User, Post, Like
from .forms import PostForm


################################
########### SCREENS ############
################################

# Homepage - All Posts Page
def index(request):
    form = PostForm()
    return render(request, "network/index.html", {"form": form})


# Following Posts Page
def following(request):
    form = PostForm()
    return render(request, "network/following.html", {"form": form})


# User Profile Page
def user(request, username: str):
    return render(request, "network/user.html", {"username": username})


################################
######## GETTER METHODS ########
################################

def get_posts(request, data):

    # JSON Serialized List
    posts_data = []

    # Parsing input data and formatting to JSON Format
    for post in data:

        if request.user.is_authenticated:
            post_dict = {
                'id': post.id,
                'body': post.body,
                'timestamp': post.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'owner': post.owner.username,
                'is_owner': post.owner.id == request.user.id,
                'is_authenticated': request.user.is_authenticated,
                'is_liked': post.like_set.filter(owner=request.user).exists(),
                'likesCount': post.likes.count()
            }

        else:
            post_dict = {
                'id': post.id,
                'body': post.body,
                'timestamp': post.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'owner': post.owner.username,
                'is_owner': False,
                'is_authenticated': False,
                'is_liked': False,
                'likesCount': post.likes.count()
            }

        # The two above cases - user authenticated or unauthenticated are separated
        # This is because we cannot query for the id of a non-existing user and so in

        posts_data.append(post_dict)

    # Returning data in JSON Serialized Format
    return posts_data


def get_all_posts(request):
    # Getting the page number from the query parameters
    page_number = request.GET.get('page', 1)

    # Getting all posts from the database
    posts = Post.objects.all().order_by('-timestamp')

    paginator = Paginator(posts, 10)  # Show 10 posts per page

    try:
        paginated_posts = paginator.page(page_number)
    except PageNotAnInteger:

        # If page is not an integer, deliver first page.
        paginated_posts = paginator.page(1)
    except EmptyPage:

        # If page is out of range (e.g. 9999), deliver last page of results.
        paginated_posts = paginator.page(paginator.num_pages)

    # Serialize the paginated posts
    posts_data = get_posts(request, paginated_posts)

    # Example of pagination information to include in JSON response
    pagination_info = {
        'has_previous': paginated_posts.has_previous(),
        'has_next': paginated_posts.has_next(),
        'previous_page_number': paginated_posts.previous_page_number() if paginated_posts.has_previous() else None,
        'next_page_number': paginated_posts.next_page_number() if paginated_posts.has_next() else None,
        'current_page_number': paginated_posts.number,
        'total_pages': paginator.num_pages,
        'page_numbers': list(paginator.page_range)
    }

    return JsonResponse({'posts': posts_data, 'pagination': pagination_info}, safe=False)


def get_following_posts(request):

    # Getting the page number from the query parameters
    page_number = request.GET.get('page', 1)

    # Getting all following user's posts from the database
    following = request.user.get_following()
    posts = Post.objects.filter(owner__in=following).order_by('-timestamp')

    paginator = Paginator(posts, 10)  # Show 10 posts per page

    try:
        paginated_posts = paginator.page(page_number)
    except PageNotAnInteger:

        # If page is not an integer, deliver first page.
        paginated_posts = paginator.page(1)
    except EmptyPage:

        # If page is out of range (e.g. 9999), deliver last page of results.
        paginated_posts = paginator.page(paginator.num_pages)

    # Serialize the paginated posts
    posts_data = get_posts(request, paginated_posts)

    # Example of pagination information to include in JSON response
    pagination_info = {
        'has_previous': paginated_posts.has_previous(),
        'has_next': paginated_posts.has_next(),
        'previous_page_number': paginated_posts.previous_page_number() if paginated_posts.has_previous() else None,
        'next_page_number': paginated_posts.next_page_number() if paginated_posts.has_next() else None,
        'current_page_number': paginated_posts.number,
        'total_pages': paginator.num_pages,
        'page_numbers': list(paginator.page_range)
    }

    return JsonResponse({'posts': posts_data, 'pagination': pagination_info}, safe=False)


def get_user(request, username: str):

    # Getting the page number from the query parameters
    page_number = request.GET.get('page', 1)

    # Getting the user by its unique username
    user = User.objects.get(username=username)

    # Getting the posts of the user with the given username
    posts = Post.objects.filter(owner=user.id).order_by('timestamp')

    # Paginate the posts
    paginator = Paginator(posts, 10)  # Show 10 posts per page

    try:
        paginated_posts = paginator.page(page_number)
    except PageNotAnInteger:

        # If page is not an integer, deliver first page.
        paginated_posts = paginator.page(1)
    except EmptyPage:
        
        # If page is out of range (e.g. 9999), deliver last page of results.
        paginated_posts = paginator.page(paginator.num_pages)

    # Serialize the paginated posts
    posts_data = get_posts(request, paginated_posts)

    # Example of pagination information to include in JSON response
    pagination_info = {
        'has_previous': paginated_posts.has_previous(),
        'has_next': paginated_posts.has_next(),
        'previous_page_number': paginated_posts.previous_page_number() if paginated_posts.has_previous() else None,
        'next_page_number': paginated_posts.next_page_number() if paginated_posts.has_next() else None,
        'current_page_number': paginated_posts.number,
        'total_pages': paginator.num_pages,
        'page_numbers': list(paginator.page_range)
    }

    user_data = {
        "username": username,
        "is_authenticated": request.user.is_authenticated,
        "is_owner": user.username == request.user.username,
        "is_following": user.followers.filter(id=request.user.id).exists(),
        "followerCount": user.followers.count(),
        "followingCount": user.following.count(),
        "posts": posts_data,
        "pagination": pagination_info
    }

    return JsonResponse({'user_data': user_data, 'pagination': pagination_info}, safe=False)


################################
######## POST METHODS ##########
################################

def add_post(request):
    if request.method == "POST":

        # Getting form information
        form = PostForm(request.POST)
        if form.is_valid():

            # Gathering data
            user = request.user
            content = form.cleaned_data['content']

            # Adding new post
            Post.objects.create(owner=user, body=content, timestamp=timezone.now())

            # Adding was successful, redirect to homepage
            return HttpResponseRedirect(reverse("index"))

    # Methods was not post, failed add post method, redirect to homepage
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


def update_post(request):
    if request.method == "POST":
        try:

            # Getting request body data
            data = json.loads(request.body)

            # Now you can access the data fields
            post_id = data.get('post_id')
            owner = data.get('owner')
            content = data.get('content')
            likes = data.get('likes')

            try:
                post = Post.objects.get(id=post_id)
            except Post.DoesNotExist:
                return JsonResponse({"status": "failed", "error": "Post not found"}, status=404)

            # User making request is not owner, tries to edit other's post
            # Not Allowed
            if request.user.username != owner and post.body != content and post.likes.count() == likes:
                return JsonResponse({"status": "failed", "error": "You are not the owner of this post"}, status=400)

            # User making request is not owner, tries to like / unlike post
            # Allowed
            elif request.user.username != owner and post.body == content and post.likes.count() != likes:

                # Like was added
                if post.likes.count() < likes:
                    Like.objects.get_or_create(owner=request.user, post=post)
                    post.is_liked = True

                # Like was removed
                else:
                    Like.objects.filter(owner=request.user, post=post).delete()
                    post.is_liked = False

            # User making request is owner, tries to edit post
            # Allowed
            elif request.user.username == owner and post.body != content and post.likes.count() == likes:
                post.body = content

            # User making request is owner, tries to like /unlike  post
            # Allowed
            elif request.user.username == owner and post.body == content and post.likes.count() != likes:

                # Like was added
                if post.likes.count() < likes:
                    Like.objects.get_or_create(owner=request.user, post=post)
                    post.is_liked = True

                # Like was removed
                else:
                    Like.objects.filter(owner=request.user, post=post).delete()
                    post.is_liked = False

            # Invalid request, both like and edit
            else:
                return JsonResponse({"status": "failed", "error": "Invalid Request"}, status=400)

            # Saving post
            post.save()

            # Assuming your update logic is successful
            return JsonResponse({"status": "success"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"status": "failed", "error": "Invalid JSON"}, status=400)

    # Methods was not post, failed follow method
    return JsonResponse({"status": "failed", "error": "Invalid Request"}, status=400)


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

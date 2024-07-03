# Imports Section
from django.urls import path
from . import views

# URL Patterns
urlpatterns = [

    # Pages
    path("", views.index, name="index"),
    path("following/", views.following, name="following"),
    path("users/<str:username>/", views.user, name="user_page"),

    # Authentication Methods
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # Endpoints - GET Method
    path("get_all_posts/", views.get_all_posts, name="get_all_posts"),
    path("get_following_posts/", views.get_following_posts, name="get_following_posts"),
    path("get_user/<str:username>/", views.get_user, name="get_user"),

    # Endpoints - POST Method
    path("add_post", views.add_post, name="add_post"),
    path("update_post/", views.update_post, name="update_post"),
    path("follow_user/<str:username>/", views.follow_user, name="follow_user"),
]

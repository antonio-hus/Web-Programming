# Imports Section
from django.urls import path
from . import views

# Web App URL Patterns
urlpatterns = [

    # Home Page
    path("", views.index, name="index"),

    # User Authentication Related Pages
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # Product Pages ( Open / Close )
    path("product/<int:product_id>", views.product, name="product_page"),

    # Product Page Editor
    path("add", views.add, name="add"),

    # User WatchList Page
    path("watchlist", views.watchlist, name="watchlist"),
    path("add_wishlist", views.add_wishlist, name="add_wishlist"),

    # Categories Related Pages
    path("category/<str:name>", views.category, name="category_page"),
    path("categories", views.categories, name="categories")
]

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("product/<int:product_id>", views.product, name="product_page"),
    path("category/<str:name>", views.category, name="category_page"),
    path("add", views.add, name="add"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add_wishlist", views.add_wishlist, name="add_wishlist"),
    path("close_listing", views.close_listing, name="close_listing"),
    path("categories", views.categories, name="categories")
]

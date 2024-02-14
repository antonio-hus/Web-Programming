from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    path("random/", views.random_page, name="random_page"),
    path("editor/", views.page_editor, name="page_editor"),
    path("editor/<str:title>", views.page_editor, name="edit"),
    path("<str:title>", views.read_entry, name="read_entry")
]

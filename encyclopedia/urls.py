from django.urls import path

from . import views

urlpatterns = [
<<<<<<< HEAD
    path("", views.index, name="index"),
    path("<str:title>", views.entry_page, name="entry_page"),
    path("search/", views.search, name="search"),
    path("create/", views.create_page, name="create"),
    path("<str:title>/edit/", views.edit_page, name="edit"),
    path("random/", views.random_page, name="random")
=======
    path("", views.index, name="index")
>>>>>>> b5b5b7483d00feb76a557f77b948d8c2460e26a9
]

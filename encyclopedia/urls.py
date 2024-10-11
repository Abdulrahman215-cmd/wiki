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
    path('', views.index, name="index"),
    path('create/', views.create_page, name='create_page'),
    path("search/", views.search, name="search"),
    path('<str:title>/', views.entry_page, name="entry"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("delete/<str:entry_name>/", views.delete, name="delete"),
    path("random", views.random_page, name="random")
>>>>>>> 7dd0e5fce470c98764fecb4223a73821664844fe
]

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('create/', views.create_page, name='create_page'),
    path("search/", views.search, name="search"),
    path('<str:title>/', views.entry_page, name="entry"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("delete/<str:entry_name>/", views.delete, name="delete"),
    path("random", views.random_page, name="random")
]

from django.urls import path

from encyclopedia import util

from . import views


app_name = "encyclopedia"



urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:TITLE>", views.TITLE_, name="title"),
    path("search", views.search, name="search"),
    path("create", views.create, name="create"),
    path("wiki/<str:TITLE>/edit", views.edit, name="edit"),
    path("random",views.random_, name="random")
]

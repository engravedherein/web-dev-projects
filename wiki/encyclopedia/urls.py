from django.urls import path

from . import views

my_app = "encyclopedia"

urlpatterns = [
    path("", views.index, name = "index"),
    path("wiki/<str:name>", views.entry, name = "entry"),
    path("search", views.search, name = "search"),
    path("newpage",views.newpage, name = "newpage"),
    path("edit",views.edit, name = "edit"),
    path("edit/<str:title>",views.editpage, name = "editpage"),
    path("random",views.random, name = "random")
]

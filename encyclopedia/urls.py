from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.load_page, name="title"),
    path("search/", views.search, name="search"),
    path("new/", views.newpage, name="newpage"),
    path("edit/", views.edit, name="edit"),
    path("save/", views.savepage, name="savepage"),
    path("rand/", views.randompage, name="randpage")
]

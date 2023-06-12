from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new_entry", views.new_entry, name="new_entry"),
    path("random_page", views.random_page, name="random_page"),
    path("edit_entry/<str:entry_title>", views.edit_entry, name="edit_entry"),
    path("wiki/<str:title1>", views.display_entry, name="display_entry")
    
]

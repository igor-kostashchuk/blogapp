from django.contrib import admin
from django.urls import path
from .views import index
from .views import create_blog
from .views import all_blog_entries
from .views import blog_details
from .views import delete_blog_entry
from .views import update_blog_entry
urlpatterns = [
    path('', index, name = "home"),
    path('entries', create_blog, name="create_blog"),
    path('entrieslist', all_blog_entries, name = 'all_blog_entries'),
    path("entries/<int:blog_id>", blog_details, name="blog_details"),
    path("entries/<int:blog_id>/delete/", delete_blog_entry, name="delete_blog_entry"),
    path("entries/<int:blog_id>/update/", update_blog_entry, name="update_blog_entry"),
    
]
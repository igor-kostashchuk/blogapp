#urls.py
from django.urls import path
from .views import registration, login
from .views import activate
from .views import logout, profile
from django.contrib.auth import views as auth_views
from .views import toggle_save_post
from .views import update_profile




urlpatterns = [path("registration/", registration,  name="registration"),
                path("login/", login, name="login"),path("activate/<uid>/<token>/",
                activate, name="activate"),
                path("logout/", logout, name="logout"),
                path("profile/<username>/", profile, name="profile"),
                path("entries/<int:blog_id>/toggle-save/", toggle_save_post, name="toggle_save_post"),
                path("profile/update/me/", update_profile, name="update_profile")]

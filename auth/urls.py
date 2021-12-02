from django.contrib import admin
from . import views
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.home, name="home"),
    path("signup", views.signup, name="signup"),
    path("login", views.signin, name="login"),
    path("logout", views.signout, name="logout"),
    path("profile", views.profile.prof, name="profile"),
    path("activate/<uid64>/<token>", views.activate, name="activate"),
]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

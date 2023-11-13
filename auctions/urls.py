from django.urls import path

from . import views

urlpatterns = [
    path("", views.active_listings, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlisting", views.create_listing, name="create_listing"),
    path("active_listings", views.active_listings, name="active_listings"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
]

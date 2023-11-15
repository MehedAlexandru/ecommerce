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
    path("watchlist", views.displayWatchlist, name="watchlist"),
    path("add_to_watchlist/<int:listing_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("remove_from_watchlist/<int:listing_id>", views.remove_from_watchlist, name="remove_from_watchlist"),
]

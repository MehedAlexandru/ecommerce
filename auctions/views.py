from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_list_or_404, render
from django.urls import reverse
from auctions.models import Auction_listings, Bids
from django.contrib.auth.decorators import login_required
from .forms import NewListingForm

from .models import User


def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


# verify if user is logged in
@login_required
def create_listing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        # validate form
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            starting_bid = form.cleaned_data["starting_bid"]
            image_url = form.cleaned_data["image_url"]
            category = form.cleaned_data["category"]
            # send data from form to database and redirect to index
            listing = Auction_listings(user=request.user, title=title, description=description,
                                       starting_bid=starting_bid, image_url=image_url, category=category)
            listing.save()
            return HttpResponseRedirect(reverse("index"))
    # if method is GET and user is logged in, display form
    else:
        form = NewListingForm()
    return render(request, "auctions/create_listing.html", {
        "form": form
        # if user is not logged in, redirect to login page. This is done by the @login_required decorator
        # the settings.py file has LOGIN_URL = '/login' which redirects to the login page
    })


def active_listings(request):
    # get all active listings
    active_listings = get_list_or_404(Auction_listings, active=True)
    return render(request, "auctions/index.html", {
        "active_listings": active_listings
    })


@login_required
def add_to_watchlist(request, listing_id):
    if request.method == "POST":
        listingData = Auction_listings.objects.get(pk=listing_id)
        currentUser = request.user
        listingData.watchlist.add(currentUser)
        listingData.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


@login_required
def remove_from_watchlist(request, listing_id):
    if request.method == "POST":
        listingData = Auction_listings.objects.get(pk=listing_id)
        currentUser = request.user
        listingData.watchlist.remove(currentUser)
        listingData.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


@login_required
def display_watchlist(request):
    currentUser = request.user
    listings = currentUser.watchlisted_items.all()
    return render(request, "auctions/watchlist.html", {"listings": listings})


def listing(request, listing_id):
    # get listing by id
    listings = Auction_listings.objects.get(pk=listing_id)
    comments = listings.comments.filter(auction=listings)
    return render(request, "auctions/listing.html", {
        "listing": listings,
        "comments": comments,
    })

def bid(request, listing_id):
    listing = Auction_listings.objects.get(pk=listing_id)
    if request.method == "POST":
        if request.user.is_authenticated:
            bid = float(request.POST["bid"])
            old_bid = float(listing.starting_bid)
            if bid > old_bid:
                listing.starting_bid = bid
                listing.winner = request.user
                listing.save()
                return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
            else:
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "message": "Bid must be higher than the current bid"
                })
        else:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "message": "You must be logged in to place a bid"
            })


def close_listing(request, listing_id):
    listing = Auction_listings.objects.get(pk=listing_id)
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.user == listing.user:
                listing.active = False
                listing.save()
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "winner": listing.winner,
                })
            else:
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "message": "You must be the owner of the listing to close the bid"
                })
        else:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "message": "You must be logged in to close the bid"
            })
        
def winned_auctions(request):
    user = request.user
    listings = Auction_listings.objects.filter(winner=user) and Auction_listings.objects.filter(active=False)
    
    return render(request, "auctions/winned_listings.html", {
        "listings": listings
    })

def add_comment(request, listing_id):
    listing = Auction_listings.objects.get(pk=listing_id)
    user = request.user
    if request.method == "POST":
        if user.is_authenticated:
            comment = request.POST["comment"]
            listing.comments.create(user=user, auction=listing, comment=comment)
            listing.save()
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        else:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "message": "You must be logged in to add a comment"
            })
            
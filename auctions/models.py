from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Auction_listings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.IntegerField()
    image_url = models.URLField(blank=True)
    category = models.CharField(max_length=64, blank=True)
    active = models.BooleanField(default=True)
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlisted_items")
    def __str__(self) -> str:
        return f"{self.title}, {self.description}, {self.starting_bid}, {self.image_url}, {self.category}, {self.active}, {self.watchlist}" 

class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    auction = models.ForeignKey(Auction_listings, on_delete=models.CASCADE, related_name="bids")
    bid = models.IntegerField()
    def __str__(self) -> str:
        return f"{self.user}, {self.auction}, {self.bid}"

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    auction = models.ForeignKey(Auction_listings, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    def __str__(self) -> str:
        return f"{self.user}, {self.auction}, {self.comment}"
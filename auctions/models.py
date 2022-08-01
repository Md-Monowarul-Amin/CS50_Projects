from datetime import datetime
from email.policy import default

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    def __str__(self):
        return self.username
    


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.name


class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description= models.CharField(max_length=64)
    starting_bid = models.IntegerField()
    image = models.URLField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete = models.CASCADE, related_name="listings")
    creation_time = models.DateField(default=datetime.now)
    watchers = models.ManyToManyField(User, blank=True, related_name= "watchlist")
    current_bid = models.IntegerField(default=starting_bid)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.title)


class Bid(models.Model):
    bid_item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    bid_price = models.IntegerField()
    bid_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f"{self.bid_owner.username}: {self.bid_price}"


class Comment(models.Model):
    item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000)
    
    def __str__(self) -> str:
        return {self.comment}


class Win(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self) -> str:
        return f"winner of {self.listing} is {self.user}"



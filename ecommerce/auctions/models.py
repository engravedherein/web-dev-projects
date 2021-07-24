from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListings(models.Model):
    item_name = models.CharField(max_length = 64)
    item_price = models.IntegerField()
    item_description = models.CharField(max_length = 225)
    item_category = models.CharField(max_length = 64,blank = True)
    item_image = models.CharField(max_length = 300,blank = True)
    created_by = models.ForeignKey(User,on_delete = models.CASCADE,blank = True )
    listing_status = models.CharField(max_length=20)
    highest_bidder = models.ForeignKey(User,on_delete = models.CASCADE, related_name='item_won',blank = True)

class Categories(models.Model):
    category = models.CharField(max_length=64)
    item = models.ForeignKey(AuctionListings,on_delete = models.CASCADE)

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete = models.CASCADE, related_name="bids")
    bid_item = models.ForeignKey(AuctionListings, on_delete = models.CASCADE ,related_name = "bidders")

class Comments(models.Model):
    commentor = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "comments")
    content = models.CharField(max_length = 300)
    item = models.ForeignKey(AuctionListings,on_delete = models.CASCADE)

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="my_watchlist")
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name="my_watchlist")
    item = models.ForeignKey(AuctionListings, on_delete = models.CASCADE, related_name= "interested_users")
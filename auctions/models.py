from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models


class AuctionBids(models.Model):
    currentBid = models.IntegerField()
    currentuserbid = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="currentuserbid",null=True)

    def __str__(self):
        return f"current bid price: {self.currentBid}"


Categorylist = ['Books','Electronics','Trading Cards','Video Games','Other']
class AuctionCategory(models.Model):
    category = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.category}"

class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    image = models.TextField()
    bid = models.ForeignKey(AuctionBids, on_delete=models.CASCADE, related_name="auctionbidding", null=True)
    # Make nullable == null=true b/c we already created objects data before hand before we created bid/comment foreign keys ,
    # therefore we ran into constraint issues of default and nonnulliable
    category = models.ForeignKey(AuctionCategory,on_delete=models.CASCADE, related_name="auctioncategory", null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="auctionowner",null=True)
    userbought = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="auctionbought",null=True)
    usersold = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="auctionsold",null=True)
    closed = models.BooleanField(default = False)

    def __str__(self):
        return self.title

class AuctionComment(models.Model):
    comment = models.CharField(max_length=255)
    auctioncomments = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comment",null=True)

    def __str__(self):
        return f"{self.comment}"

class User(AbstractUser,models.Model):
    userwatchlist = models.ManyToManyField(AuctionListing, related_name="userwatch", blank=True)
    usercommentlist = models.ForeignKey(AuctionComment,related_name="usercomment", null=True, on_delete=models.CASCADE,blank=True) 
    
    #Instead of referring to User directly, you should reference the user model using django.contrib.auth.get_user_model(). 
    #This method will return the currently active user model – the custom user model if one is specified, or User otherwise.








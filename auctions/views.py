from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *


def index(request):
    return render(request, "auctions/index.html",{
        'auctionlisting': AuctionListing.objects.all()
    })


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


def auction_list(request, id):
    listing = AuctionListing.objects.get(pk=id)
    userid = request.user.id
    user = User.objects.get(id=userid)

    watching = bool(User.objects.filter(userwatchlist__id=id))
    print(watching)

    def test():
        if watching:
            return 'Watching'
        else:
            return 'Add To Watchlist'
    test()
    
    if request.method == 'POST':
        if request.POST.get('addwatch', False):
            if watching:
                watching = False
                user.userwatchlist.remove(listing)
                return render(request, "auctions/auctionlist.html", {
                    "listing": listing,
                    'watchstatus': test()
                })                
            else:
                user.userwatchlist.add(listing)
                watching = True
                return render(request, "auctions/auctionlist.html", {
                    "listing": listing,
                    'watchstatus': test(),
                })          

        if request.POST.get('current',False):
            a = int(request.POST["current"])
            if a <= listing.bid.currentBid:
                return render(request, 'auctions/auctionlist.html',{
                    "listing": listing,
                    "message": 'Your Current bid does not meet the minimum',
                    'watchstatus': test(),
                })
            else:
                listing.bid.currentBid = a
                listing.bid.save() # save foreign key reference first.
                return render(request, "auctions/auctionlist.html", {
                "listing": listing,
                'watchstatus': test(),
                })

    return render(request, "auctions/auctionlist.html", {
        "listing": listing,
        'watchstatus': test()
    })



def create_list(request):
    if request.method == "POST":
        c = AuctionBids(currentBid = request.POST['bid'])
        c.save()        
        category = request.POST['category']
        b = AuctionListing(title=request.POST['title'], description = request.POST['description'],image = request.POST['image'],bid= c)
        if AuctionCategory.objects.filter(category=category):
            e = AuctionCategory.objects.get(category=category)
            e.save()
            b.category = e
        else:
            f = AuctionCategory(category=category)
            f.save()
            b.category = f
        b.save()
        
        return HttpResponseRedirect(reverse('auctionlist', args=(b.id,) ))
    
    return render(request, "auctions/createlisting.html",{
        'Categories': Categorylist,
    })

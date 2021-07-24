from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect

from .models import User

from auctions.models import AuctionListings, User, Watchlist, Bid, Comments, Categories


def index(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        initial_bid = request.POST["initial_bid"]
        image_URL = request.POST["image_url"]
        category = request.POST.get("category")
        current_user = request.user
        status = 'active'
        highest_bidder = request.user
        obj = AuctionListings(
                            item_name=title,
                            item_price=initial_bid,
                            item_category = category,
                            item_description=description,
                            item_image=image_URL,
                            created_by = current_user,
                            listing_status = status,
                            highest_bidder = highest_bidder
                            )
        obj.save()

        if category:
            cat_obj = Categories(category = category, item = obj)
            cat_obj.save()
            
    return render(request, "auctions/index.html",{
                "heading": "All Listings",
                "list_items" : AuctionListings.objects.all()
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

def active_listing(request):
    return render(request,"auctions/index.html",
    {
        "heading" : "Active Listings",
        "list_items" : AuctionListings.objects.filter(listing_status='active').all()
    })

def create_listing(request):
    return render(request,"auctions/create_listing.html")

def listings(request,id):

    message = "free"  
    if request.method == "POST":

        if request.POST.getlist('bid_amount'):

            current_item = AuctionListings.objects.get(pk = id)
            bid_amount = request.POST["bid_amount"]
            
            # bid_obj = Bid(bidder = request.user, bid_item = current_item)
            # bid_obj.save()
            
            if(int(bid_amount) > current_item.item_price):
                current_item.item_price = bid_amount
                current_item.highest_bidder = request.user
                current_item.save(update_fields=['item_price','highest_bidder'])
                message = "no message required in listing.html"
            else:
                message = ""
    
        elif request.POST.get("comment_text"):
            commentor = request.user
            commented_text = request.POST["comment_text"]
            item = AuctionListings.objects.get(pk = id)
            comm_obj = Comments(commentor = commentor, 
                                content= commented_text,
                                item = item)
            comm_obj.save()

        else:
            obj = AuctionListings.objects.get(pk = id)
            obj.listing_status = 'Closed'
            obj.save(update_fields=['listing_status'])

    wlist = []

    if request.user.is_authenticated:
        wlist = Watchlist.objects.filter(user = request.user).all()
    
    comms = Comments.objects.filter(item = AuctionListings.objects.get(pk = id)).all()

    return render(request,"auctions/listing.html",{
                "item" : AuctionListings.objects.get(pk = id),
                "watchlist" : wlist, #Watchlist.objects.filter(user = request.user).all(),
                "message" : message,
                "comment_list": comms
            })

def watchlist(request):
    return render(request,"auctions/watchlist.html",{
        "watchlist": Watchlist.objects.filter(user=request.user).all()
    })

def add_to_watchlist(request,item_id):
    # old_list = Watchlist.objects.filter(user = request.user).values('item')

    # if AuctionListings.objects.get(pk = item_id) in old_list:
    #     return render(request,"auctions/watchlist.html",{
    #     "message" : "Item already in the "
    # })

    watchlist_obj = Watchlist(user = request.user, item = AuctionListings.objects.get(pk = item_id))
    watchlist_obj.save()
    return listings(request,item_id)
  
    
def remove_from_watchlist(request,item_id):
    item_to_remove = AuctionListings.objects.get(pk = item_id)
    Watchlist.objects.filter(user = request.user, item = item_to_remove).delete()
    if request.META.get("HTTP_REFERER")[22:] == "watchlist":
        return render(request,"auctions/watchlist.html",{
            "watchlist" : Watchlist.objects.filter(user = request.user).all(),
        })
    else:
        return listings(request,item_id)


def categories(request):
    return render(request,"auctions/categories.html",{
        "categories" : Categories.objects.values('category').distinct()#order_by().values_list('category',flat=True).distinct()
    })


def category(request,cat):
    act_list = Categories.objects.filter(category = cat).all()
    final_list = []
    for i in act_list:
        if i.item.listing_status == 'active':
            final_list.append(i.item)

    return render(request,"auctions/index.html",{
        "heading" : cat+'s',
        "list_items" : final_list
    })
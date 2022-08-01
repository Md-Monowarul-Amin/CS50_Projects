from datetime import datetime
from operator import is_
import re
from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import is_valid_path, reverse
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from requests import request
from django.contrib.auth.decorators import login_required

import auctions


from .models import *

class NewAuctionForm(forms.Form):
    title = forms.CharField(label="title", max_length=64)
    description = forms.CharField(widget=forms.Textarea)
    starting_bid = forms.IntegerField(label="starting_bid")
    image = forms.URLField(label="image Url", required=False)
    # category = forms.Select(choices=Category.objects.all())
    # category = forms.Select(attrs={'class': 'form-control'})

def index(request, winning_message = None, category = None):
    if category == None:
        auctions = AuctionListing.objects.all()
    else:
        auctions = AuctionListing.objects.filter(category = category)
    curr_user = request.user
    return render(request, "auctions/index.html",{"auctions":auctions, "curr_user": curr_user, "winning_message": winning_message, "categories": Category.objects.all(), "selected_category": category})


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


@login_required
def create_auction(request):
    if request.method == "POST":
        form = NewAuctionForm(request.POST)
        if form.is_valid():
            print("IS valid")
            title = form.cleaned_data['title']
            category_ = Category.objects.get(pk = request.POST["category"])
            description = form.cleaned_data["description"]
            image = form.cleaned_data["image"]
            print(image)
            created_by = request.user
            creation_time = datetime.now()
            starting_bid = (form.cleaned_data['starting_bid'])
            AuctionListing.objects.create(title=title, description= description, starting_bid= starting_bid, 
            image = image,category = category_, created_by= created_by, creation_time= creation_time, current_bid = starting_bid, is_active = True)
            
            print(starting_bid)
            return HttpResponseRedirect(reverse("index"))

        else:
            print("NOT VALID") 
        user = request.user
        # print(category, title)
       
    user = request.user
    category = Category.objects.all()
    create_auction_form = NewAuctionForm()
    return render(request, "auctions/create_auction.html",{"form": create_auction_form, "categories":category}) 


def listing(request, listing_id):
    auction_listing = AuctionListing.objects.get(pk= listing_id)
    try:
        watched_by = auction_listing.watchers.get(username = request.user.username)
        in_watchlist = True
    except ObjectDoesNotExist:
        in_watchlist = False
    # print(watched_by)
    # in_watchlist = False
    """for person in watched_by:
        if person == request.user:
            in_watchlist = True
            break"""

    print(auction_listing.current_bid)
    try:
        curr_bid_owner = Bid.objects.get(bid_price = auction_listing.current_bid)
    except ObjectDoesNotExist:
        curr_bid_owner = None
    comments = Comment.objects.filter(item = auction_listing)
    message = ''
    
    try:
        win_ = Win.objects.filter(listing = auction_listing)
        for win in win_:
            if request.user == win.user:
                message = "Congratulations!! You Won " + auction_listing.title
                AuctionListing.objects.get(pk= listing_id).delete()
                # Win.objects.get(listing = auction_listing).delete()
            
    except ObjectDoesNotExist:
        message = None
    
    return render(request, "auctions/listing.html", {"listing": auction_listing, "watchlist":in_watchlist, "curr_bid_owner": curr_bid_owner, "comments": comments, "message": message})


@login_required
def create_bid(request, listing_id):
    if request.method == "POST":
        bid_item = AuctionListing.objects.get(pk= listing_id)
        bid_price = request.POST["bidprice"]
        bid_owner = request.user
        if int(bid_price) > bid_item.current_bid:
            bid_item.current_bid = bid_price
            bid_item.save()
            Bid.objects.create(bid_item= bid_item, bid_price= bid_price, bid_owner = bid_owner)
            
            return render(request, "auctions/listing.html", {"listing": bid_item})
        else:
            return render(request, "auctions/listing.html", {"listing": bid_item, "message": "Your bid is less than the current_bid"})


def AddToWatchList(request, listing_id):
    listing = AuctionListing.objects.get(pk= listing_id)
    listing.watchers.add(request.user)
    listing.save()
    print("Watcher Added")
    return index(request)


def VisitWatchList(request):
    user = request.user
    Auction_listings = AuctionListing.objects.all()
    user_watched = []
    for auction in Auction_listings:
        for user_ in auction.watchers.all():
            if user_ == user:
                user_watched.append(auction)
    return render(request, "auctions/watchlist.html", {"auctions":user_watched, "curr_user": request.user})
    

def RemoveFromWatchList(request, listing_id):
    listing = AuctionListing.objects.get(pk= listing_id)
    user = request.user
    listing.watchers.remove(user)
    return VisitWatchList(request)


@login_required
def AddComment(request, listing_id):
    if request.method == "POST":
        listing_ = AuctionListing.objects.get(pk= listing_id)
        user = request.user
        comment = request.POST["comment"]
        Comment.objects.create(item = listing_, user = user, comment= comment)

        return listing(request, listing_id)


def CloseAuction(request, listing_id):
    listing_ = AuctionListing.objects.get(pk= listing_id)
    try:
        curr_bid = Bid.objects.get(bid_price = listing_.current_bid)
    except ObjectDoesNotExist:
        AuctionListing.objects.get(pk= listing_id).delete()
        winnig_message = "No Bid Yet"
        return index(request, winning_message = winnig_message)
    winner = curr_bid.bid_owner
    auction_win = Win.objects.create(listing = listing_, user = winner)
    auction_win.save()
    print(auction_win)
    listing_.is_active = False
    listing_.save()
    # AuctionListing.objects.get(pk= listing_id).delete()
    winnig_message = "Auction Closed " + "winner " + winner.username
    return index(request, winning_message = winnig_message)
    


def SelectCategory(request, category_id):
    category = Category.objects.get(pk= category_id)
    # auction_listing = AuctionListing.objects.filter(category = category)
    return index(request, category= category)


def VisitCategory(request):
    category = Category.objects.all()
    return render(request, "auctions/categories.html", {"categories": category})


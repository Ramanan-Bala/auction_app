from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Category, Listing, Watchlist, Bid, Comment
from . import utils


def index(request):
    lists = utils.get_listing()
    category = Category.objects.all()
    wCount = utils.get_len_watchlist(request.user)
    return render(request, "auctions/index.html", {
        "lists": lists,
        "title": "All Listing",
        "wCount": wCount,
        "cat": category
    })


def activeListing(request):
    lists = Listing.objects.exclude(active=False).all()
    category = Category.objects.all()
    wCount = utils.get_len_watchlist(request.user)
    return render(request, "auctions/index.html", {
        "lists": lists,
        "title": "Active Listing",
        "wCount": wCount,
        "cat": category
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


@login_required(login_url="login")
def createAuction(request):
    category = Category.objects.all()
    wCount = utils.get_len_watchlist(request.user)
    return render(request, "auctions/createAuction.html", {
        "cat": category,
        "wCount": wCount
    })


def submit(request):
    if request.method == "POST":
        title = request.POST["title"]
        category = request.POST["category"]
        startingBid = request.POST["startingBid"]
        imageUrl = request.POST["imageUrl"]
        description = request.POST["description"]
        if request.user == "AnonymousUser":
            return render(request, "auction/createAuction.html", {
                "message": "Please login and create auction"
            })
        else:
            category_obj = Category.objects.get(id=category)
            list = Listing(
                title=title,
                description=description,
                category=category_obj,
                startingBid=startingBid,
                currentBid=startingBid,
                createdBy=request.user
            )
            if len(imageUrl) > 10:
                list.image = imageUrl
            list.save()
            return HttpResponseRedirect(reverse("index"))


def watchList(request):
    watchList = Watchlist.objects.filter(user=request.user)
    items = []
    for watch in watchList:
        listId = watch.list.id
        items.append(Listing.objects.get(id=watch.list.id))

    return render(request, "auctions/watchList.html", {
        "lists": items,
        "wCount": len(watchList),
    })


def addWatchlist(request, listId):
    list = Listing.objects.get(id=listId)
    userComments = Comment.objects.filter(list=list)
    w = Watchlist.objects.filter(list=list, user=request.user)
    context = {"list": list,
               "added": True, "comments": userComments}
    if len(w) == 0 and list.active:
        Watchlist.objects.create(user=request.user, list=list)
        wCount = utils.get_len_watchlist(request.user)
        context["wCount"] = wCount
        context["success"] = "Auction added to wishlist"
        return render(request, "auctions/listingPage.html", context)
    else:
        wCount = utils.get_len_watchlist(request.user)
        context["wCount"] = wCount
        context["error"] = "Auction already in wishlist"
        return render(request, "auctions/listingPage.html", context)


def removeWatchlist(request, listId):
    list = Listing.objects.get(id=listId)
    userComments = Comment.objects.filter(list=list)
    w = Watchlist.objects.filter(list=list, user=request.user)
    if len(w) > 0:
        w.delete()
        wCount = utils.get_len_watchlist(request.user)
        return render(request, "auctions/listingPage.html", {
            "list": list,
            "wCount": wCount,
            "success": "Auction removed from Watchlist",
            "comments": userComments
        })
    else:
        wCount = utils.get_len_watchlist(request.user)
        return render(request, "auctions/listingPage.html", {
            "list": list,
            "wCount": wCount,
            "error": "Auction already removed from Watchlist",
            "comments": userComments
        })


def listingPage(request, listId):
    list = Listing.objects.get(id=listId)
    userComments = Comment.objects.filter(list=list)
    wCount = utils.get_len_watchlist(request.user)
    if User.is_authenticated:
        try:
            if Watchlist.objects.get(user=request.user, list=list):
                added = True
        except:
            added = False
    else:
        added = False
    return render(request, "auctions/listingPage.html", {
        "list": list,
        "wCount": wCount,
        "added": added,
        "comments": userComments
    })


def category(request, category):
    l = Listing.objects.filter(category__category=category)
    cat = Category.objects.all()
    wCount = utils.get_len_watchlist(request.user)
    return render(request, "auctions/index.html", {
        "lists": l,
        "cat": cat,
        "wCount": wCount,
        "header": "yes", "c": category
    })


@login_required(login_url="login")
def bidding(request, listId):
    list = Listing.objects.get(id=listId)
    userComments = Comment.objects.filter(list=list)
    if request.method == "POST":
        bidAmount = int(request.POST["bid"])
        if User.is_authenticated:
            try:
                if Watchlist.objects.get(user=request.user, list=list):
                    added = True
            except:
                added = False
        else:
            added = False
        wCount = utils.get_len_watchlist(request.user)
        context = {"list": list,
                   "wCount": wCount,
                   "added": added, "comments": userComments}
        if bidAmount > list.currentBid:
            list.currentBid = bidAmount
            list.save()
            bid = Bid.objects.filter(list=list)
            bid.delete()
            print(request.user)
            newBid = Bid(user=request.user, list=list, price=bidAmount)
            newBid.save()
            context["success"] = "Bid successful"
            return render(request, "auctions/listingPage.html", context)
        else:
            context["error"] = f"Bid must be greater than {list.currentBid}"
            return render(request, "auctions/listingPage.html", context)


@login_required(login_url="login")
def submitComment(request, listId):
    list = Listing.objects.get(id=listId)
    userComments = Comment.objects.filter(list=list)
    if request.method == "POST":
        comment = request.POST["comment"]
        if User.is_authenticated:
            try:
                if Watchlist.objects.get(user=request.user, list=list):
                    added = True
            except:
                added = False
        else:
            added = False
        wCount = utils.get_len_watchlist(request.user)
        context = {"list": list,
                   "wCount": wCount,
                   "added": added,
                   "comments": userComments
                   }
        com = Comment(user=request.user, list=list, comment=comment)
        com.save()
        return render(request, "auctions/listingPage.html", context)


@login_required(login_url="login")
def closeBid(request, listId):
    list = Listing.objects.get(id=listId)
    wCount = utils.get_len_watchlist(request.user)
    userComments = Comment.objects.filter(list=list)
    if User.is_authenticated:
        try:
            if Watchlist.objects.get(user=request.user, list=list):
                added = True
        except:
            added = False
    else:
        added = False
    if list.createdBy == request.user and list.active:
        bid = Bid.objects.filter(list=list)
        if len(bid) > 0:
            bid = Bid.objects.get(list=list)
            list.buyer = bid.user
            list.active = False
            list.save()
            return render(request, "auctions/listingPage.html", {
                "list": list,
                "wCount": wCount,
                "added": added,
                "comments": userComments,
                "success": "Bid Closed"
            })
        else:
            return render(request, "auctions/listingPage.html", {
                "list": list,
                "wCount": wCount,
                "added": added,
                "comments": userComments,
                "error": "No bids yet... Can't close the bid"
            })
    else:
        return render(request, "auctions/listingPage.html", {
            "list": list,
            "wCount": wCount,
            "added": added,
            "comments": userComments,
            "error": "Bid already Closed"
        })

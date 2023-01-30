from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.urls import reverse

# Create your views here.
from .models import Category, Listing, User


def register(request):
    if request.method == 'POST':
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        User.objects.create_user(username, email, password)
    else:
        return render(request, "register.html")


def loginUser(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("listing"))
    else:
        return render(request, "login.html")


def listing(request):
    listing = Listing.objects.all()
    return render(request, "listing.html", {
        "listing": listing
    })


def addListing(request):
    if request.method == 'POST':
        title = request.POST["title"]
        categoryId = int(request.POST["category"])
        startingBid = request.POST["startingBid"]
        description = request.POST["description"]
        category = Category.objects.get(pk=categoryId)
        list = Listing(
            title=title,
            category=category,
            startingBid=startingBid,
            description=description,
            createdBy=request.user
        )
        list.save()
        return HttpResponseRedirect(reverse("listing"))
    else:
        category = Category.objects.all()
        return render(request, "add_listing.html", {"category": category})

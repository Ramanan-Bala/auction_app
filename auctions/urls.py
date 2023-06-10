from django.urls import path

from . import views

urlpatterns = [
    path("", views.activeListing, name="activeListing"),
    path("allListing", views.index, name="index"),
    path("category/<str:category>", views.category, name="category"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createAuction", views.createAuction, name="createAuction"),
    path("submitAuction", views.submit, name="submitAuction"),
    path("watchList", views.watchList, name="watchList"),
    path("addWatchlist/<int:listId>",
         views.addWatchlist, name="addWatchlist"),
    path("removeWatchlist/<int:listId>",
         views.removeWatchlist, name="removeWatchlist"),
    path("listingPage/<int:listId>", views.listingPage, name="listingPage"),
    path("bidding/<int:listId>", views.bidding, name="bidding"),
    path("comment/<int:listId>", views.submitComment, name="submitComment"),
    path("closeBid/<int:listId>", views.closeBid, name="closeBid"),
]

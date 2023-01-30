from django.contrib import admin
from django.urls import path
from .views import register, loginUser, listing, addListing

urlpatterns = [
    path('register/', register, name="register"),
    path('login/', loginUser, name="login"),
    path('listing/', listing, name="listing"),
    path('add-listing/', addListing, name="add-listing"),
]

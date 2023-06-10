from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


class Category(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.category}"


class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100, null=True, blank=True)
    startingBid = models.FloatField()
    currentBid = models.FloatField(
        null=True, blank=True)
    comments = models.CharField(max_length=100, null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="similarListing")
    createdBy = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="allCreations", blank=True)
    watcher = models.ManyToManyField(
        User, blank=True, related_name="watchedListing")
    buyer = models.ForeignKey(
        User, null=True, on_delete=models.PROTECT, blank=True)
    image = models.CharField(
        max_length=1000, default="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS6V_R6WMnHzN5bpexR-vQ1tNickx9phBGTHA&usqp=CAU")
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - Rs.{self.startingBid} - {self.category}"


class Watchlist(models.Model):
    list = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="userWatchlist")

    def __str__(self):
        return f"Personal watchlist for {self.user} - {self.list}"


class Bid(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="userBid")
    list = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="userBidList")
    price = models.DecimalField(
        max_digits=6, decimal_places=2)

    def __str__(self):
        return f"bid on item: {self.list} by {self.user} with price: {self.price}"


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    list = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="usercomments")
    comment = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return f"comment on: {self.list} by {self.user} with: {self.comment}"

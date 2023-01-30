from django.contrib import admin

from auction.models import Category, Listing, User

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing)

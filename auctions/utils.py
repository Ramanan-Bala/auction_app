from .models import Category, Listing, Watchlist


def get_category():
    return Category.objects.all().order_by('id').reverse()


def get_listing():
    return Listing.objects.all()


def get_len_watchlist(u):
    try:
        watchList = Watchlist.objects.filter(user=u)
        wCount = len(watchList)
    except TypeError:
        wCount = None
    return wCount

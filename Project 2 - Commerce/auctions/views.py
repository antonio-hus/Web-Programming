from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing, ProductCategory, Bid, Comment
from decimal import Decimal


# Forms Below
class ListingForm(forms.Form):
    title = forms.CharField(max_length=64, label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Title..."}))
    description = forms.CharField(max_length=256, label='', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': "Description..."}))
    image_url = forms.CharField(max_length=256, label='', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Image Link..."}))
    category = forms.ModelChoiceField(queryset=ProductCategory.objects.all(), label='', required=False, empty_label="Select a category", widget=forms.Select(attrs={'class': 'form-select'}))
    start_bid = forms.DecimalField(label='', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': "Starting Bid..."}))


# Views Below
# Home Page
def index(request):
    """
    Returns a homepage containing all listings on the website
    """
    active_listings = Listing.objects.filter(status=True)
    closed_listings = Listing.objects.filter(status=False)
    return render(request, "auctions/index.html",
                  {"active_listings": active_listings, "closed_listings": closed_listings})


# User Authentication Related Views
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


# Product Page View
def product(request, product_id):
    """
    Returns the Product Page given by the product's ID
    :param product_id: Integer Number ( Listing's Primary Key )
    """

    # Finding Product and Comments to Render
    the_product = Listing.objects.filter(id=product_id).first()

    # Checking if the Product Auction Status is Open (True)
    # Display accordingly

    if the_product.status:
        comments = the_product.comments.all()

        # Users signed in can watchlist an item ( Item initally not watchlisted )
        wishlist_status = False
        if request.user.is_authenticated:
            wishlist_status = request.user.wishlist.filter(id=product_id).exists()

        # Registering a Bid
        # Minimum Bids Condition
        if the_product.current_price == 0:
            minimum_bid = the_product.start_price
        else:
            minimum_bid = the_product.current_price + Decimal('0.1')*the_product.start_price

        # Getting POST Form Data
        if request.method == "POST":

            # Submitting the new Bid Form
            if "bid" in request.POST:
                proposed_bid = request.POST.get("bid")

                # Saving new current_price and adding a new bidder
                the_product.current_price = proposed_bid
                the_product.save()

                new_bid = Bid(listing=the_product, bidder=request.user, bid=proposed_bid)
                new_bid.save()

            if "rating" in request.POST:
                title = request.POST.get("title")
                rating = request.POST.get("rating")
                description = request.POST.get("description")

                proposed_comment = Comment(reviewer=request.user, listing=the_product,
                                           title=title, rating=rating, description=description)
                proposed_comment.save()

            # Closing the Auction Form
            else:
                the_product.status = False
                the_product.save()

            return HttpResponseRedirect(reverse('product_page', kwargs={"product_id": product_id}))

        return render(request, "auctions/listing.html", {"product": the_product, "comments": comments,
                                                         "wishlist_status": wishlist_status, "minimum_bid": minimum_bid})
    else:
        # Computing Winner
        winner = None
        winner_bid = None
        last_bid = the_product.bids.last()
        if last_bid:
            winner = last_bid.bidder.username
            winner_bid = last_bid.bid
            # NOTE: ACTUAL PAYMENT HANDLING WOULD GO HERE

        return render(request, "auctions/listing.html", {"product": the_product, "winner": winner, "price": winner_bid})


# Add a new Listing Functionality
def add(request):
    """
    Renders Listing Editor Page
    Collects submitted data and adds a new Listing ( containing or not the optional fields )
    """
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            seller = request.user
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            category = form.cleaned_data["category"]
            image_url = form.cleaned_data["image_url"]
            start_bid = form.cleaned_data["start_bid"]
            current_bid = 0

            if category and image_url:
                new_listing = Listing(seller=seller, title=title, description=description, category=category, photo=image_url, start_price=start_bid, current_price=current_bid)
            elif category:
                new_listing = Listing(seller=seller, title=title, description=description, category=category,
                                      start_price=start_bid, current_price=current_bid)
            elif image_url:
                new_listing = Listing(seller=seller, title=title, description=description,
                                      photo=image_url, start_price=start_bid, current_price=current_bid)
            else:
                new_listing = Listing(seller=seller, title=title, description=description,
                                      start_price=start_bid, current_price=current_bid)

            new_listing.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = ListingForm()
    return render(request, "auctions/add.html", {"form": form})


# Watch List Page
def watchlist(request):
    """
    Renders the user's watchlist
    """
    user = request.user
    items = user.wishlist.all()

    # Removing watch listed auctions that are no longer active
    for item in items:
        if not item.status:
            user.wishlist.remove(item)

    return render(request, "auctions/watchlist.html", {"items": items})


# Add / Remove from Watch List Feature
def add_wishlist(request):
    """
    Allows users to add to their watch list if the product was not added yet
    Otherwise, allows users to remove from the wishlist
    """
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        product = Listing.objects.filter(id=product_id).first()
        if product:
            if not request.user.wishlist.filter(id=product_id).exists():
                request.user.wishlist.add(product)
            else:
                request.user.wishlist.remove(product)
    return HttpResponseRedirect(reverse('watchlist'))


# Categories Related Pages
def categories(request):
    """
    Renders all categories from our store
    """
    categs = ProductCategory.objects.all()
    return render(request, "auctions/categories.html", {"categories": categs})


def category(request, name):
    """
    Renders all open auctions from a given category
    """
    category = ProductCategory.objects.filter(category=name).first()
    products = Listing.objects.filter(category=category, status=True)
    return render(request, "auctions/category.html", {"category_name": name, "products": products})

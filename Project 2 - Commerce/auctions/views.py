from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing, ProductCategory


# Forms Below
class ListingForm(forms.Form):
    title = forms.CharField(max_length=64, label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Title..."}))
    description = forms.CharField(max_length=256, label='', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': "Description..."}))
    image_url = forms.CharField(max_length=256, label='', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Image Link..."}))
    category = forms.ModelChoiceField(queryset=ProductCategory.objects.all(), label='', required=False, empty_label="Select a category", widget=forms.Select(attrs={'class': 'form-select'}))
    start_bid = forms.DecimalField(label='', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': "Starting Bid..."}))


# Views Below
def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {"listings": listings})


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


def product(request, product_id):
    the_product = Listing.objects.filter(id=product_id).first()
    comments = the_product.comments.all()
    wishlist_status = False
    if request.user.is_authenticated:
        wishlist_status = request.user.wishlist.filter(id=product_id).exists()
    if request.method == "POST":
        pass
    return render(request, "auctions/listing.html", {"product": the_product, "comments": comments, "wishlist_status": wishlist_status} )


def close_listing(request):
    pass


def add(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            seller = request.user
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            category = form.cleaned_data["category"]
            image_url = form.cleaned_data["image_url"]
            start_bid = form.cleaned_data["start_bid"]
            current_bid = start_bid

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


def watchlist(request):
    user = request.user
    items = user.wishlist.all()
    return render(request, "auctions/watchlist.html", {"items": items})


def add_wishlist(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        product = Listing.objects.filter(id=product_id).first()
        if product:
            if not request.user.wishlist.filter(id=product_id).exists():
                request.user.wishlist.add(product)
            else:
                request.user.wishlist.remove(product)
    return HttpResponseRedirect(reverse('watchlist'))


def categories(request):
    categs = ProductCategory.objects.all()
    return render(request, "auctions/categories.html", {"categories": categs})


def category(request, name):
    category = ProductCategory.objects.filter(category=name).first()
    products = Listing.objects.filter(category=category)
    return render(request, "auctions/category.html", {"category_name": name, "products": products})

from typing import ContextManager
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max
from django.contrib import messages
from .forms import AuctionForm, BidForm, CommentForm



from .models import User, Auction, Bids, Comments


def index(request):
    items = Auction.objects.all()
    context = {'items': items}
    return render(request, "auctions/index.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")



def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))



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
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request):
    form = AuctionForm()
    if request.method == 'POST':
        # use request.FILES to save images to databses
        form = AuctionForm(request.POST, request.FILES)
        if form.is_valid():
            # save the instance in a variable before committing
            instance = form.save(commit=False)
            # modify the 'creator' attribute to the current active user
            instance.creator = request.user
            instance.save()
        return HttpResponseRedirect(reverse("auctions:index"))
        # print(request.POST) = print dict to debug
    context = {'form': form}
    return render(request, "auctions/create.html", context)


# +Bids
def listings(request, item_id):
    item = Auction.objects.get(id = item_id)
    form = BidForm()
    form2 = CommentForm()
    context={}
    if request.method == 'POST':
        form = BidForm(request.POST)

        if form.is_valid():
            new_bid = form.save(commit=False)
            current_bids = Bids.objects.filter(auction = item)
            is_highest_bid = all(new_bid.bidding_price > bid.bidding_price for bid in current_bids)
            is_valid_bid = new_bid.bidding_price > item.price
            
            if is_highest_bid and is_valid_bid:
                new_bid.auction = item
                new_bid.person_bidding = request.user
                new_bid.save()
                messages.success(request, 'Successful bid')

            else:
                messages.error(request, 'Bid is too low')

        return HttpResponseRedirect(reverse("auctions:listings", args=[item_id]))
    
    total_bids = Bids.objects.filter(auction = item).count()
    total_comments = Comments.objects.filter(auction = item).count()
    current_bid = Bids.objects.filter(auction = item).aggregate(Max('bidding_price'))['bidding_price__max']
    # print(total_bids)
    # print(current_bid)
    if total_bids > 0:
        bid = Bids.objects.filter(auction = item).get(bidding_price = current_bid)
        context['person'] = bid.person_bidding
    if total_comments > 0:
        comments = Comments.objects.filter(auction = item)
        context['comments'] = comments

    context['item'] = item
    context['form'] = form
    context['current_bid'] = current_bid
    context['bids'] = total_bids
    context['user'] = request.user
    context['form2'] = form2
    context['total_comments'] = total_comments
    
    return render(request, "auctions/listing.html" , context)

@login_required
def delete(request, item_id):
    item = Auction.objects.get(id = item_id)
    if request.method == 'POST':
        if request.user == item.creator:
            Auction.objects.filter(id= item_id).delete()
            return HttpResponseRedirect(reverse("auctions:index"))

@login_required
def end_auction(request, item_id):
    item = Auction.objects.get(id = item_id)
    if request.method == 'POST':
        if request.user == item.creator:
            item.has_ended = True
            item.save()
    return HttpResponseRedirect(reverse("auctions:index"))

@login_required
def comments(request, item_id):
    item = Auction.objects.get(id = item_id)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.auction = item
            new_comment.user = request.user
            new_comment.save()
    
    return HttpResponseRedirect(reverse("auctions:listings", args=[item_id]))

@login_required
def add_wishlist(request, item_id):
    if request.method == "POST":
        item = Auction.objects.get(id= item_id)
        if item.watchers.filter(id = request.user.id).exists():
            item.watchers.remove(request.user)
        else:
            item.watchers.add(request.user)

    return HttpResponseRedirect(reverse("auctions:listings", args=[item_id]))

@login_required
def remove_wishlist(request, item_id):
    if request.method == "POST":
        item = Auction.objects.get(id= item_id)
        if item.watchers.filter(id = request.user.id).exists():
            item.watchers.remove(request.user)
        else:
            item.watchers.add(request.user)
    return HttpResponseRedirect(reverse("auctions:wishlist"), )


def wishlist(request):
    wishlist = Auction.objects.filter(watchers = request.user)
    context = {}
    context['wishlist'] = wishlist
    return render(request, "auctions/wishlist.html", context)


def category(request, cat):
    category_items = Auction.objects.filter(category=cat)
    context = {'items': category_items, 'category' : cat.title()}
    return render(request, 'auctions/categories.html', context)
        


        
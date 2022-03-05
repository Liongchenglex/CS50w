from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, time
from django.db.models.deletion import CASCADE

from django.db.models.fields import DateTimeField


class User(AbstractUser):
    def __str__(self):
        return self.username



class Auction(models.Model):
    item_name = models.CharField(max_length = 100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description  = models.CharField(max_length= 100, blank=True, null=True)
    image = models.ImageField(default="media/images/default.jpeg", blank=True, null=True, upload_to="media/images/")
    date_uploaded = models.DateTimeField(default=datetime.now, blank=True)
    DURATIONS = [
        (3, "Three Days"),
        (7, "One Week"),
        (14, "Two Weeks")
    ]
    duration = models.IntegerField(choices=DURATIONS)
    creator = models.ForeignKey(User, null=True, on_delete= models.CASCADE)
    CATEGORIES = [
            ('home', "Home"),
            ('sports', "Sports"),
            ('clothings', "Clothings"),
            ('books', "Books"),
            ('others', "Others")
            ]   
    category = models.CharField(choices=CATEGORIES, max_length=10)
    watchers = models.ManyToManyField(User, blank=True, null=True, related_name='watchlist')
    has_ended = models.BooleanField(default=False)

    def __str__(self):
        return f"Auction #{self.id}: {self.item_name}"

    class Meta:
        ordering = ('-date_uploaded', )



class Bids(models.Model):
    bidding_price = models.DecimalField(max_digits=10, decimal_places=2)
    auction = models.ForeignKey(Auction, related_name='bids', on_delete=models.CASCADE)
    person_bidding = models.ForeignKey(User, related_name='person', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Bids'
    
    def __str__(self):
        return f"Bid #{self.id}: {self.bidding_price} on {self.auction.item_name} by {self.person_bidding.username}"



class Comments(models.Model):
    message = models.TextField(max_length=300)
    time = DateTimeField(default=datetime.now)
    auction = models.ForeignKey(Auction, related_name= 'comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-time', )


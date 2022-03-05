
from django.forms.widgets import Widget
from .models import Auction, Bids, Comments
from django import forms

class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['item_name', 'price', 'description', 'image', 'duration', 'category']
        widgets = {'price': forms.NumberInput(attrs={"placeholder": "USD$"})}

    item_name=forms.CharField( widget=forms.TextInput(
        attrs={"placeholder": "Name",
            "size":40
        }))

    description = forms.CharField( required=False, widget= forms.Textarea(attrs={"placeholder": "Describe your Product"}))


class BidForm(forms.ModelForm):
    class Meta:
        model = Bids
        fields =['bidding_price']
        labels= {'bidding_price': 'Bidding Price'}
        widgets = {'bidding_price': forms.NumberInput(attrs={"placeholder": "USD$"})}
        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['message']
        labels = {'message' : ''}
        widgets = {'message' : forms.Textarea(attrs={'cols': 100, 'rows': 5})}
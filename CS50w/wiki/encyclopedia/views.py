from django.forms.widgets import Textarea
from django.shortcuts import render
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from random import choice

from . import util

# no cascading effect. index can call function search whihc is below

class NewPageForm(forms.Form):
    title = forms.CharField(label = 'title')
    # text area to have cursor start from top
    content = forms.CharField(label= 'content', widget=forms.Textarea)

class EditForm(forms.Form):
    body = forms.CharField( widget=forms.Textarea, label=False)


def index(request):
    '''
    Display the list of available encyclopedia pages
    Allow user to search query in input box
    '''
    # 'q' is a parameter in the browser search
    # https://stackoverflow.com/questions/150505/capturing-url-parameters-in-request-get
    if request.GET.get('q'):
        return search(request, request.GET['q'])
        # must always have have a return
        # GET['q'] stores the parameter of 'q'
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })
    # the optional third argument(dictionary) is called a context



def entry(request, entry):
    '''
    Display the entry selected
    Allow the user to search query in the input box
    '''
    contents = util.get_entry(entry)
    # to allow GET
    if request.GET.get('q'):
        return search(request, request.GET['q'])
    if contents is None:
        return render(request, "encyclopedia/search_result.html", {
            "title": entry
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "contents": contents,
            "entry": entry
        })


def search(request , query):
    '''
    Processing the query from the input box 
    If entry has some characters of the query, return those list of entries
    If entry has no characters of the query, return a page that prompts user to create new page
    '''
    contents = util.get_entry(query)
    entries = util.list_entries()
    # make query case insensitive
    low_query = query.lower()
    # store entries that contain the query
    fuzzy_search = []
    if contents is None:
        for entry in entries:
            low_entry = entry.lower()
            if low_query in low_entry:
                fuzzy_search.append(entry)
        return render(request, "encyclopedia/search_result.html", {
            "entries": fuzzy_search,
            "search" : query
        })
    else:
        return HttpResponseRedirect(reverse('encyclopedia:entry', args=[query] ))



def create_new_page(request):
    """
    Allows user to create new page
    Redirects the user to the new page created
    If entry already exists, an error message is displayed
    Allows user to input query in input box
    """
    if request.GET.get('q'):
        return search(request, request.GET['q'])
    if request.method == "POST":
        # populating the NewPageForm with post info
        form = NewPageForm(request.POST)
        # check that forms are filled with correct values
        entries = util.list_entries()
        if form.is_valid():
            # cleaned data from NewPageForm()
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            for entry in entries:
                new_title = title.lower()
                new_entry = entry.lower()
                if new_entry == new_title:
                    return HttpResponse(f"Error, entry {title} already exists!")
        util.save_entry(title, content)
        # use redirect whenever after POST
        # reverse will give the url mapping of encyclopedia:entry(name) >> /wiki/<str:entry>
        # args needed when url takes in an argument >> <str:entry>=title
        return HttpResponseRedirect(reverse('encyclopedia:entry', args=[title] ))
    else:
        return render(request, "encyclopedia/new_page.html", {
            "form": NewPageForm()
        })



def edit(request, entry):
    """
    Allows user to edit existing entries
    Textarea will be pre-populated by existing information
    Redirects user to edited page after submission
    Allows user to input query in input box
    """
    if request.GET.get('q'):
        return search(request, request.GET['q'])
    contents = util.get_entry(entry)
    if request.method == "POST":
        # POST data submitted; process data
        form = EditForm(request.POST)
        if form.is_valid():
            contents = form.cleaned_data['body']
            util.save_entry(entry, contents)
        return HttpResponseRedirect(reverse('encyclopedia:entry', args=[entry] ))
    else:
        # Initial request; pre-fill form with current entry
        form = EditForm(initial={'body' : contents})
        return render(request, "encyclopedia/edit.html", {
            "form": form,
            "entry": entry
        })

def random(request):
    """
    Randomly generates an entry page
    """
    entries = util.list_entries()
    random = choice(entries)
    return HttpResponseRedirect(reverse('encyclopedia:entry', args=[random]))





        

        


# Imports Section
# --- Django Related Imports ---
from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

# --- UTILS ---
from . import util

# --- MISC ---
from markdown2 import markdown
import random
import re

# Forms
class EntryForm(forms.Form):
    title = forms.CharField(label="", max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Title goes here...'}))
    content = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'Content goes here...'}))


# Views Definition Section

def index(request):
    """
    Home Page
    Returns a page containing all entries in the encyclopedia
    """
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })

def read_entry(request, title: str):
    """
    Entry Page
    Returns the html version of the .md file named :title:
    Returns the 404 page if file not found
    """
    entry = util.get_entry(title)
    if entry:
        title = title.capitalize()
        entry_html = markdown(entry)
        return render(request, "encyclopedia/entry_page.html", {
            "title": title,
            "entry_html": entry_html
        })
    else:
        return render(request, "encyclopedia/404_page.html", {
            "title": title
        })
    
def search(request):
    """
    Search Page
    Returns the full match page of the query if found
    Returns the relevant partial matches for the given query, if it is not a full match
    Returns the homepage for an empty query, otherwise
    """
    query = request.GET.get('q')
    if query != "":
        page = util.get_entry(query)
        if page:
            title = query.capitalize()
            entry_html = markdown(page)
            return render(request, "encyclopedia/entry_page.html", {"title": title, "entry_html": entry_html})
        else:
            entries = util.list_entries()
            relevant_entries = []
            for entry in entries:
                if re.search(query, entry, re.IGNORECASE):
                    relevant_entries.append(entry)
            return render(request, "encyclopedia/search.html", {"entries": relevant_entries})
    else:
        entries = util.list_entries()
        return render(request, "encyclopedia/index.html", {"entries": entries})

def random_page(request):
    """
    Random Page
    Returns a random entry page
    """
    entries = util.list_entries()
    return read_entry(request, random.choice(entries))

def page_editor(request, title=""):
    """
    Editor (Add/Edit) Page
    Returns a page where the user can add/edit an entry
    """
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():

            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)

            return HttpResponseRedirect(reverse('encyclopedia:read_entry', args=[title]))
    else:
        if title == "":
            form = EntryForm()
        else:
            content = util.get_entry(title)
            form = EntryForm(initial={"title": title, "content":content})
    return render(request, "encyclopedia/entry_editor.html", {"form":form})


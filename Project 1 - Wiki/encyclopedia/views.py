# Imports Section
# --- Django Related Imports ---
from django.shortcuts import render
from django.http import HttpResponse

# --- UTILS ---
from . import util

# --- MISC ---
from markdown2 import markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def read_entry(request, title: str):
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


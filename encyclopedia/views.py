<<<<<<< HEAD
from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util
import random
import markdown2

class searchform(forms.Form):
    query = forms.CharField()

class CTform(forms.Form):
    title = forms.CharField(label="TITLE")
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter Content Here', 'rows': 18, 'cols': 90}), label='')

class EditForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 23, 'cols': 92}), label="")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    }) 

def entry_page(request, title):
    single_entry = util.get_entry(title)
    if single_entry is None:
        return  render(request, "encyclopedia/error.html", {
            "message": "Page Not Found"
            })
    else:
        html_content = markdown2.markdown(single_entry)
        return render(request, "encyclopedia/entry.html", {
            "single_entry": html_content,
            "title": title
            })


def search(request):
    if request.method == "POST":
        form = searchform(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            single_entry = util.get_entry(query)
            if single_entry is None:
                all_entries = util.list_entries()

                partial_matches = []
                for entry in all_entries:
                    if query.lower() in entry.lower():
                        partial_matches.append(entry)
                if partial_matches:
                    return render(request, "encyclopedia/search_results.html", {
                        "partial_matches": partial_matches
                    })
                else:
                    return render(request, "encyclopedia/error.html", {
                        "message": "Page Not Found!"
                    })
            else:
                html_content = markdown2.markdown(single_entry)
                return render(request, "encyclopedia/entry.html", {
                    "single_entry": html_content,
                    "title": query
                })
    else:
        return render(request, "encyclopedia/layout.html", {
            "form": searchform()
        })
    
def create_page(request):
    if request.method == "POST":
        form = CTform(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            created = util.get_entry(title)
            if created is None:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("entry_page", args=[title]))
            else:
                return render(request, "encyclopedia/error.html", {
                    "message": "A Page With That Title Already Exist!"
                })
    return render(request, "encyclopedia/create.html", {
        "form": CTform()
    })

def edit_page(request, title):
    content = util.get_entry(title)
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content'].replace('\r', '')
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry_page", args=[title]))
    else:
        form = EditForm(initial={'content': content})
    return render(request, "encyclopedia/edit.html", {
        "form": form,
        "title": title
    })

def random_page(request):
    every_entry = util.list_entries()
    random_entry = random.choice(every_entry)
    if random_entry is not None:
        return HttpResponseRedirect(reverse("entry_page", args=[random_entry]))
    return render(request, "encyclopedia/layout.html")
=======
from django.shortcuts import render, redirect

import markdown2

import random

from django.urls import reverse

from . import util

from django.core.files.storage import default_storage

from .util import get_entry

def index(request):
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })

def entry_page(request, title):
    content = get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {"message": "Page not found.","title": title, "content": content})
    else:
        html_content = markdown2.markdown(content)
        return render(request, "encyclopedia/entry.html", {"title": title, "content": html_content, "entry_title": title})
     
def search(request,):
    query = request.GET.get('q')
    entries = util.list_entries()

    if query.lower() in [entry.lower() for entry in entries]:
        return redirect('entry', title=query)

    results = []
    for entry in entries:
        if query.lower() in entry.lower():
            results.append(entry)
     
    return render(request, "encyclopedia/search_results.html", {
        "query": query,
        "results": results,
    })

def create_page(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        
        if default_storage.exists(f"entries/{title}.md"):
            return render(request, 'encyclopedia/create_page.html', {
                'error': "An entry with this title already exists."
            })
        
        util.save_entry(title, content)
        
        return redirect('entry', title=title)
    
    return render(request, 'encyclopedia/create_page.html')

def normalize_line_endings(content):
    return content.replace('\r\n', '\n').replace('\r', '\n')

def edit(request, title):
    content = get_entry(title)
    if request.method == "POST":
        content = request.POST['content']
        content = normalize_line_endings(content)
        util.save_entry(title, content)
        return redirect('entry', title=title)
    content = normalize_line_endings(content)
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })

def delete(request, entry_name):
    if request.method == "POST":
        if request.POST.get("confirm") == "true":
            util.delete_entry(entry_name)
            return redirect("index")
        else:
            return render(request, "encyclopedia/confirmation.html", {
                "entry_title": entry_name
            })
        
def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return redirect(reverse('entry', args=[random_entry]))

>>>>>>> 7dd0e5fce470c98764fecb4223a73821664844fe

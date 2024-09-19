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


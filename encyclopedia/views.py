from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

<<<<<<< HEAD
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
>>>>>>> b5b5b7483d00feb76a557f77b948d8c2460e26a9

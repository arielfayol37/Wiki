from django.shortcuts import render, redirect
from markdown2 import markdown
from . import util
from django import forms
from django.urls import reverse
from random import randint

class SearchForm(forms.Form):
    title1 = forms.CharField(label='', max_length=100,\
        widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

class InputForm(forms.Form):
    title_field = forms.CharField(label='Enter a title for your Entry:', max_length=100)
    textarea_field = forms.CharField(label='Type the content of your entry here', widget=forms.Textarea)

class EditForm(forms.Form):
    textarea_field =  forms.CharField(label='Type the content of your entry here', widget=forms.Textarea)

def mdtitle_to_html(title):
    md_content = util.get_entry(title)
    if md_content == None:
        return [] # Using a list here to iterate over nothing
                  # in the html, hence executing the default
                  # which will be the error page
    else:
        html_content = markdown(md_content)
    return [html_content]


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), "form": SearchForm()
    })

def display_entry(request, title1):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            title1 = form.cleaned_data['title1'].lower()
            html = mdtitle_to_html(title1)  
            if html == []: # In case title1 is not found among the entries
                search_entries = [] # attempting to find whethere title1 is a
                                    # substring of one or many of the entries
                for entry in util.list_entries():
                    if title1 in entry.lower():
                        search_entries.append(entry)
                if search_entries:
                    return render(request, "encyclopedia/search.html", {
        "entries": search_entries, "form": form
    })    
            return render(request, "encyclopedia/entry.html", {"content": html,\
                                                               "title1": title1,\
                                                                "form":SearchForm()})
        else:
            index(request)
    html = mdtitle_to_html(title1) 
    return render(request, "encyclopedia/entry.html", {"content": html,\
                                                       "title1": title1,\
                                                        "form":SearchForm()})



def new_entry(request):
    form = InputForm() 
    error, title = "", ""
    save = True
    posted = False
    if request.method == "POST":
        form = InputForm(request.POST)
        posted = form.is_valid()
        if posted:
            # Retrieve markdown content and save it
            title = form.cleaned_data["title_field"].strip()
            if title in util.list_entries():
                error = f"Entry with title {title} already exists.\n \
                    <h5>Note that titles are case sensitive<h5>"
                posted = False
            else:
                save = False
                md_content = form.cleaned_data["textarea_field"]
                util.save_entry(title, md_content)
                return redirect(reverse('display_entry', kwargs={'title1': title}))
        else:
            error = "Invalid Entry. Check your content"
    
    return render(request, "encyclopedia/new_entry.html",
                  {"post_form": form, "posted": posted, "error": error,\
                    "save": save,"new_entry_title":title, "form":SearchForm()})
def edit_entry(request, entry_title):
    md_content = util.get_entry(entry_title)
    edit_form = EditForm()
    edit_form.fields['textarea_field'].initial = md_content
    save = True
    error = ""
    posted = False
    if request.method == "POST":
        edit_form = EditForm(request.POST)
        posted = edit_form.is_valid()
        if posted:
            save = False
            new_md_content = edit_form.cleaned_data["textarea_field"]
            util.save_entry(entry_title,new_md_content)
            edit_form = ""
        else:
            error = "Invalid Entry. Check your content"

    return render(request, "encyclopedia/edit_entry.html",{"edit_form":edit_form,\
                                                           "entry_title1": entry_title,\
                                                            "posted":posted,\
                                                            "save":save,
                                                            "error": error,
                                                            "form":SearchForm()})

def random_page(request):
    entries = util.list_entries()
    r = randint(0, len(entries)) # inclusive of both bounds
    r = 0 if r < 0 else r-1
    return display_entry(request,entries[r])
"""
def new_entry(request):
    posted = False
    form = InputForm() 
    error = ""
    save = True
    if request.method == "POST":
        form = InputForm(request.POST)
        posted = form.is_valid()
        if posted:
            # Retrive markdown content and save it
            title = form.cleaned_data["title_field"].strip()
            if title in util.list_entries():
                error = "Entry already exists"
                posted = False
                return render(request, "encyclopedia/new_entry.html",\
                               {"post_form": form, "posted":posted, "error":error,\
                                "save":save})
            md_content = form.cleaned_data["textarea_field"]
            util.save_entry(title, md_content)
            return render(request, "encyclopedia/new_entry.html",
                           {"post_form":"", "posted":posted, "error":error,\
                                "save":save})
        else:
            error = "Invalid Entry. Check your content"
            return render(request, "encyclopedia/new_entry.html",\
                               {"post_form": form, "posted":posted, "error":error,\
                                "save":save})
         
    return render(request, "encyclopedia/new_entry.html", \
                  {"post_form":form, "posted":posted, "error":error,\
                                "save":save})
"""
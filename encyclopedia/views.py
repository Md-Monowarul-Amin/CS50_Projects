import imp
import markdown2
from django.http import HttpResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from markdown2 import Markdown
from django.urls import reverse
from django import forms
import random

from . import util

class NewEntyForm(forms.Form):
    title = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)


class EditForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)

def index(request):
    print(util.list_entries())
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def TITLE_(request, TITLE):
    to_markdown = Markdown()
    entry_title = TITLE
    entry_body =  util.get_entry(TITLE)
    if entry_body == None:
        return render(request, "encyclopedia/error.html", {"message": f"{entry_title} does not Exist"})
    return render(request, "encyclopedia/title.html", {
        "entry": to_markdown.convert(entry_body), "title" : entry_title 
    })

def search(request):
    # 
    if request.method == 'POST':
        # print("inside search")
        s_value = request.POST.get('q')
        #  print(request.POST.get('q'))
        # print(s_value)
        list_ = util.list_entries()
        # print(list_)
        if s_value in list_:
            return TITLE_(request, s_value)
        else:
            list_item = []
            # print(s_value)
            for item in list_:
                # print(item)
                if s_value.upper() in item.upper():
                    # print(item)
                    list_item.append(item)
            return render(request, "encyclopedia/search.html", {"list_item":list_item, "item":s_value})

def create(request):
    if request.method == "POST":
        form = NewEntyForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            message = form.cleaned_data["message"]
            if util.get_entry(title) == None:
                util.save_entry(title, message)
                return TITLE_(request,title)
            else:
                return render(request, "encyclopedia/error.html", {"message": f"{title} Already  Exists", "visit":True, "title":title})
    else:
        return render(request, "encyclopedia/create.html", {"form": NewEntyForm()})
    

def edit(request, TITLE):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data["message"]
            util.save_entry(TITLE, message)
            return TITLE_(request,TITLE)

    entry = util.get_entry(TITLE)
    form = EditForm(initial={
        "message": entry
    })
    
    return render(request, "encyclopedia/edit.html", {"form":form, "title":TITLE})


def random_(request):
    entry_list = util.list_entries()
    random_item = random.choice(entry_list)
    return TITLE_(request,random_item)


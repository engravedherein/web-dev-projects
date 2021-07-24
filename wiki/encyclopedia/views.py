from django.shortcuts import render
from markdown2 import Markdown
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from random import randint
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, name):
    got_entry = util.get_entry(name)

    if got_entry == None:
        return render(request,"not_found/notFound.html",{ "name": name })
    
    else:
        markdowner = Markdown()
        content = markdowner.convert(got_entry)
 
        return render(request, "encyclopedia/entry.html",
        {
            "body":content,
            "name":name
        })

def search(request):
    if request.method == "GET":
        to_search = request.GET.get('q','')
        if util.get_entry(to_search) != None:
            return entry(request,to_search)
        else:
            all_entries = util.list_entries()
            matching_list = []

            for element in all_entries:
                if (element.lower()).find(to_search.lower()) != -1:
                    matching_list.append(element)
            flag = True
            if(matching_list == []):
                flag = False

            return render(request,"encyclopedia/search_results.html",
            {
                "entries":matching_list,
                "flag" : flag
            })

def newpage(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')

        if title in util.list_entries():
            return render(request, "encyclopedia/error.html", {"title":title})
        util.save_entry(title,content)
        return entry(request,title)
    return render(request,"encyclopedia/new_page.html")

def edit(request):
    return render(request,"encyclopedia/edit_list.html",{"entries" : util.list_entries() })

def editpage(request,title):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        util.save_entry(title,content)
        return entry(request,title)

    content = util.get_entry(title)
    return render(request, "encyclopedia/edit_page.html", {
        "title":title,
        "content" : content
    })

def random(request):
    all_entries = util.list_entries()
    r = randint( 0,len(all_entries)-1 )
    return entry(request,all_entries[r])
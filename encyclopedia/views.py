import random
from django.shortcuts import render
from django.http import HttpResponse
import markdown2
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def md_to_html(page_title):
    mdcontent = util.get_entry(page_title) 
    if mdcontent is None:
        return None
    else:
        return markdown2.markdown(mdcontent)
    

def load_page(request, title):
    page_body = md_to_html(title)
    if page_body is None:
        return render(request, "encyclopedia/err.html", {
            "message": "Entry does not exist"
        })
    
    return render(request, "encyclopedia/title.html", {
        "page_title": title,
        "page_body": page_body
    })

def search(request):
    if request.method == "POST":
        page_title = request.POST['q']
        page_body = md_to_html(page_title)
        if page_body:
            return render(request, "encyclopedia/title.html", {
                "page_title": page_title,
                "page_body": page_body
            })
        else:
            allent = util.list_entries()
            recom = []
            for ent in allent:
                if page_title.lower() in ent.lower():
                    recom.append(ent)
            
            if recom:
                return render(request, "encyclopedia/index.html",{
                    "entries": recom
                })
            
            return render(request, "encyclopedia/err.html", {
                "message": "No entries with this name"
            })
        
def pageexist(title):
    allent = util.list_entries()
    for ent in allent:
        if title.lower() == ent.lower():
            return True
    return False
        
def newpage(request):
    if request.method == "POST":
        page_title = request.POST["title"]
        if pageexist(page_title):
            return render(request, "encyclopedia/err.html",{
                "message": "Entry already exist"
            })
        else:
            mdcontent = request.POST["body"]
            util.save_entry(page_title, mdcontent)
            page_body = md_to_html(page_title)
            return render(request, "encyclopedia/title.html",{
                "page_title": page_title,
                "page_body": page_body
            })
    else:
        return render(request, "encyclopedia/new.html")
    
def edit(request):
    if request.method == "POST":
        page_title = request.POST.get("title")
        content = util.get_entry(page_title)
        return render(request, "encyclopedia/edit.html", {
            "page_title": page_title,
            "content": content
        })
    
def savepage(request):
    if request.method == "POST":
        page_title = request.POST.get('title')
        content = request.POST.get('body')
        util.save_entry(page_title, content)
        page_body = md_to_html(page_title)
        return render(request, "encyclopedia/title.html",{
            "page_title": page_title,
            "page_body": page_body
        })
    
def randompage(request):
    allent = util.list_entries()
    page_title = random.choice(allent)
    page_body = md_to_html(page_title)
    return render(request, "encyclopedia/title.html",{
        "page_title": page_title,
        "page_body": page_body
    })
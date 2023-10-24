from django.shortcuts import render
from markdown import Markdown
import random

from . import util


def convertMdToHtml(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    htmlContent = convertMdToHtml(title)
    if htmlContent == None:
        return render(request, "encyclopedia/error.html", {
            "message": "This entry does not exist"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": htmlContent
        })


def search(request):
    if request.method == "POST":
        entrySearch = request.POST['q']
        htmlContent = convertMdToHtml(entrySearch)
        if htmlContent is not None:
            return render(request, "encyclopedia/entry.html", {
            "title": entrySearch,
            "content": htmlContent
        })
        else:
            allEntries = util.list_entries()
            recommend = []
            for entry in allEntries:
                if entrySearch.lower() in entry.lower():
                    recommend.append(entry)
            return render(request, "encyclopedia/search.html", {
                "recommend": recommend,
            })
        
def newPage(request):
    if request.method == 'GET':
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        titleExist = util.get_entry(title)
        if titleExist is not None:
            return render(request, 'encyclopedia/error.html', {
                'message': "Entry page already exists"
            })
        else:
            util.save_entry(title, content)
            htmlContent = convertMdToHtml(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": htmlContent
            })
        

def edit(request): 
    if request.method == "POST":
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, 'encyclopedia/edit.html', {
            "title": title,
            "content": content,
        })
    

def saveEdit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        htmlContent = convertMdToHtml(title)
        return render(request, 'encyclopedia/entry.html', {
            'title': title,
            'content': content,
        })
    

def rand(request):
    allEntries = util.list_entries()
    randEntry = random.choice(allEntries)
    htmlContent = convertMdToHtml(randEntry)
    return render(request, 'encyclopedia/entry.html', {
        'title': randEntry,
        'content': htmlContent
    })
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item
from .forms import CreateNewList


# https://docs.djangoproject.com/en/3.1/topics/forms/#field-data
# Create your views here.

# Create the different views for the webiste and handle http requests
# dynamic rendering
# def index(response,id):
#  return HttpResponse("<h1>%s</h1>" % id)

def index(response,id):
    # querying using the id. (int)
    ls = ToDoList.objects.get(id=id)
    
    # check if the todolist is in the user
    # if ls in response.user.todolist.all():
    
    if response.method == "POST":
        print(response.POST)
        # this post request will get information from the whole form in list.html
        # so if we click save, then it will pass a dict to here
        # looking like: {"save":["save"], "c1":["clicked"]}  // if c1 is clicked if not it will be empty
        
        # if save doesn't exist, it will be None
        # button1: save checked items status
        if response.POST.get("save"): # put name of btn
            for item in ls.item_set.all():
                # if we query and get "c" + id and is clicked, then we set the complete field to true
                if response.POST.get("c" + str(item.id)) == "clicked":
                    item.complete = True
                else:
                   item.complete = False
                item.save() # save it
        # button2: add new items
        # get the text in the input field in list.html when we press the newItem btn
        elif response.POST.get("newItem"):
            txt = response.POST.get("new")
            # validate if its valid input
            if len(txt) > 2:
                ls.item_set.create(text = txt, complete = False)
            else:
                print("Something went wrong")

    return render(response,"main/list.html",{"ls":ls})


def home(response):
    return render(response,"main/home.html",{})



def create(response):
    
    # response.user // get the user
    if response.method == "POST":
        form = CreateNewList(response.POST) # dict

        if form.is_valid():
            n = form.cleaned_data['name']   # get data from input
            t = ToDoList(name=n)
            t.save()    # save to db
            
            # save data to specific user
            # reponse.user.todolist.add(t)

        # redirecting
        return HttpResponseRedirect("/%i"%t.id)
    else:
        form = CreateNewList()

    return render(response,"main/create.html",{"form":form}) 


def view(response):
    return render(response, "main/view.html", {})




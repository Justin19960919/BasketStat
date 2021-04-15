### django ajax resources ###
'''
https://simpleisbetterthancomplex.com/tutorial/2016/08/29/how-to-work-with-ajax-request-with-django.html
https://simpleisbetterthancomplex.com/tutorial/2016/11/15/how-to-implement-a-crud-using-ajax-and-json.html
https://www.pluralsight.com/guides/work-with-ajax-django

'''
from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.core import serializers
from .forms import FriendForm
from .models import Friend


#creates the FriendForm object, takes all the friends objects from the database, and sends them to the index.html template,
def indexView(request):
    form = FriendForm()
    friends = Friend.objects.all()
    return render(request, "my_app/index.html", {"form": form, "friends": friends})


# ajax post view, ajax views can only deal with json
# so, we need JsonResponse, serialize
def postFriend(request):
    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "POST":
        # get the form data
        form = FriendForm(request.POST)
        # save the data and after fetch the object in instance
        if form.is_valid():
            instance = form.save()
            # serialize in new friend object in json
            ser_instance = serializers.serialize('json', [ instance, ])
            # send to client side.
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"error": form.errors}, status=400)

    # some error occured
    return JsonResponse({"error": ""}, status=400)



def checkNickName(request):
    # request should be ajax and method should be GET.
    if request.is_ajax and request.method == "GET":
        # get the nick name from the client side.
        nick_name = request.GET.get("nick_name", None)
        # check for the nick name in the database.
        if Friend.objects.filter(nick_name = nick_name).exists():
            # if nick_name found return not valid new friend
            return JsonResponse({"valid":False}, status = 200)
        else:
            # if nick_name not found, then user can create a new friend.
            return JsonResponse({"valid":True}, status = 200)

    return JsonResponse({}, status = 400)



### Class based view example

'''
-- views.py
class FriendView(View):
    form_class = FriendForm
    template_name = "index.html"

    def get(self, *args, **kwargs):
        form = self.form_class()
        friends = Friend.objects.all()
        return render(self.request, self.template_name, 
            {"form": form, "friends": friends})

    def post(self, *args, **kwargs):
        if self.request.is_ajax and self.request.method == "POST":
            form = self.form_class(self.request.POST)
            if form.is_valid():
                instance = form.save()
                ser_instance = serializers.serialize('json', [ instance, ])
                # send to client side.
                return JsonResponse({"instance": ser_instance}, status=200)
            else:
                return JsonResponse({"error": form.errors}, status=400)

        return JsonResponse({"error": ""}, status=400)
-- urls.py
path("", FriendView.as_view(), name = "friend_cbv"),


-- index.js
// other previous stuff
$.ajax({
    type: 'POST',
    url: "{% url 'friend_cbv' %}", // CHANGE the POST url
    // ... continues
// ...


'''

def test(request):
    return render(request, "my_app/test.html") 

























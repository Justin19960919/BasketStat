from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect

# Create your views here.

# import player models
from .models import PlayerRecord, Player

# Login required for Class based views
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

# Generic Views
# from django.views.generic import (ListView, 
#                                   DetailView, 
#                                   CreateView,
#                                   UpdateView,
#                                   DeleteView)
# for Ajax
from django.http import JsonResponse
from django.core import serializers
from django.template.loader import render_to_string
from .forms import PlayerForm


def player_list(request):
	player_form  = PlayerForm()
	players = Player.objects.all()
	return render(request, 'player/player_list.html', {'form': player_form, 'players': players})



# ajax post view, ajax views can only deal with json
# so, we need JsonResponse, serialize
def postPlayer(request):
    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "POST":
        print('got into view function')
        # get the form data
        form = PlayerForm(request.POST)
        
        # save the data and after fetch the object in instance
        # need to do checks here if username of number already exists

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






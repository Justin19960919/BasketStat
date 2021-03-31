from django.shortcuts import render, redirect
from django.contrib import messages
# import player models
from .models import PlayerRecord, Player
from django.contrib.auth.decorators import login_required

from .forms import PlayerForm


@login_required
def player_list(request):
    if request.method == 'POST':
        print(request.POST)
        
        form = PlayerForm(request.POST)
        if form.is_valid():
            # Check if number and name is taken
            addform = form.save(commit = False)
            addform.belongsTo = request.user
            # check if already exists before save
            # returns a boolean
            if Player.objects.filter(name=addform.name, number=addform.number).exists():
                # put out message
                messages.info(request, f"Found a duplicate name and number!")
                return redirect('player-list')
            # else
            addform.save()
        return redirect('player-list')
        
    else:
        user = request.user
        player_form  = PlayerForm()
        print(request.user)
        players = Player.objects.filter(belongsTo = user)
        print("Players: ", players)
        # render page
        return render(request, 'player/player_list.html', {'form': player_form, 'players': players})


def delete_player(request, id):
    
    p = Player.objects.get(id = id)
    p.delete()
    return redirect('player-list')











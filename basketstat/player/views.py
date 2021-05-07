from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum
from django.db.models import Avg
from django.views import View

# import player models
from .models import Player
from game.models import PlayerRecord

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

# forms
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
                messages.warning(request, f"Found a duplicate name and number!")
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




class DisplayPlayerStats(LoginRequiredMixin, View):


  def get(self, request, player_id):

    player, player_records = self.getAllPlayerRecords(player_id)
    stat = self.getPlayerAggregation(player_records)
    
    profile = {
      'name': player.name,
      'number': player.number,
      'stat': stat,
    }


    return render(request, 'player/player_stat.html', {'profile': profile})


  def roundStats(self, a, b):
    return round(a/b, 2) if b!=0 else 0


  def getAllPlayerRecords(self, player_id):
    player = Player.objects.get(id=player_id)
    player_records = PlayerRecord.objects.filter(playerId=player)
    return player, player_records


  def getPlayerRecordsFromXGames(self, player_id, x):
    player_records = self.getAllPlayerRecords(player_id)
    player_records = player_records.order_by('gameId__dateOfGame')
    numberOfGames = len(player_records)

    if numberOfGames < x:
        x = numberOfGames

    player_records = player_records[len(player_records) - x: ]
    return player_records


  def getPlayerAggregation(self, player_records):
      # Aggregate
      totalTwoPointers = player_records.aggregate(Sum('twoPointers'))['twoPointers__sum']
      totalTwoPointersMade = player_records.aggregate(Sum('twoPointersMade'))['twoPointersMade__sum']
      ##
      AvgTwoPointPercentage = self.roundStats(totalTwoPointersMade, totalTwoPointers)
   
      totalThreePointers = player_records.aggregate(Sum('threePointers'))['threePointers__sum']
      totalThreePointersMade = player_records.aggregate(Sum('threePointersMade'))['threePointersMade__sum']
      ##
      AvgThreePointPercentage = self.roundStats(totalThreePointersMade, totalThreePointers)

      totalFreeThrows = player_records.aggregate(Sum('freethrows'))['freethrows__sum']
      totalFreeThrowsMade = player_records.aggregate(Sum('freethrowMade'))['freethrowMade__sum']
      ##
      AvgFreeThrowPercentage = self.roundStats(totalFreeThrowsMade, totalFreeThrows)
 
      AvgTwoPointers = round(player_records.aggregate(Avg('twoPointers'))['twoPointers__avg'], 2)
      AvgThreePointers = round(player_records.aggregate(Avg('threePointers'))['threePointers__avg'], 2)
      AvgFT = round(player_records.aggregate(Avg('freethrows'))['freethrows__avg'], 2)
      ppg = AvgTwoPointers * 2 + AvgThreePointers * 3


      AvgOr = round(player_records.aggregate(Avg('offensiveRebound'))['offensiveRebound__avg'], 2)
      AvgDr = round(player_records.aggregate(Avg('defensiveRebound'))['defensiveRebound__avg'], 2)
      AvgBlk = round(player_records.aggregate(Avg('block'))['block__avg'], 2)
      AvgStl = round(player_records.aggregate(Avg('steal'))['steal__avg'], 2)
      AvgAst = round(player_records.aggregate(Avg('assist'))['assist__avg'], 2)
      AvgTo = round(player_records.aggregate(Avg('turnover'))['turnover__avg'], 2)
      AvgDf = round(player_records.aggregate(Avg('offensiveFoul'))['offensiveFoul__avg'], 2)
      AvgOf = round(player_records.aggregate(Avg('defensiveFoul'))['defensiveFoul__avg'], 2)
      AvgMins = round(player_records.aggregate(Avg('numberOfMinutesPlayed'))['numberOfMinutesPlayed__avg'], 2)

      data = {
        'PPG': ppg,
        'Avg2P': AvgTwoPointers,
        'Avg3P': AvgThreePointers,
        'AvgFT': AvgFT,
        'Avg2PP': AvgTwoPointPercentage,
        'Avg3PP': AvgThreePointPercentage,
        'AvgFTP': AvgFreeThrowPercentage,
        'AvgOr': AvgOr,
        'AvgDr': AvgDr,
        'AvgBlk': AvgBlk,
        'AvgStl': AvgStl,
        'AvgAst': AvgAst,
        'AvgTo': AvgTo,
        'AvgDf': AvgDf,
        'AvgOf': AvgOf,
        'AvgMins': AvgMins
      }

      return data




















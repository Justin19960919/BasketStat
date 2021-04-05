from django import forms
from .models import Game
from player.models import Player


class CreateGameForm(forms.ModelForm):
    class Meta:
        model = Game
        # specify which fields
        fields = ['players','season', 'opponent', 'area', 'dateOfGame', 
              'nameOfGame', 'gameUrl']



    # now when initializing CreateGameForm, we have one more parameter, user
    def __init__(self, user, *args, **kwargs):
        super(CreateGameForm, self).__init__(*args, **kwargs)
        self.fields['players'].queryset = Player.objects.filter(belongsTo=user)

    # in model forms: default query set is .objects.all()
    players = forms.ModelMultipleChoiceField(queryset=Player.objects.all(),
        widget=forms.CheckboxSelectMultiple)
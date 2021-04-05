from django.contrib import admin
from .models import Game, Comments, PlayerRecord
# Register your models here.
# game_models = [Game, Comments, PlayerRecord]
# admin.site.register(game_models)
admin.site.register(Game)
admin.site.register(Comments)
admin.site.register(PlayerRecord)
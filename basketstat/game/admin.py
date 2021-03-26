from django.contrib import admin
from .models import Game, Comments
# Register your models here.
game_models = [Game, Comments]
admin.site.register(game_models)
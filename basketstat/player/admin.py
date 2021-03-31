from django.contrib import admin
from .models import PlayerRecord, Player

# Register your models here.
myModels = [PlayerRecord, Player]
admin.site.register(myModels)
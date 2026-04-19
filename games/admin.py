from django.contrib import admin
from .models import Game, Playlist, Subscription, Purchase

admin.site.register(Game)
admin.site.register(Playlist)
admin.site.register(Subscription)
admin.site.register(Purchase)
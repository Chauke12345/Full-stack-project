from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from .models import Playlist

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_playlist(sender, instance, created, **kwargs):
    if created:
        Playlist.objects.create(user=instance)
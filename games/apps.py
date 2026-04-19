from django.apps import AppConfig
def ready(self):
    import games.signals


class GamesConfig(AppConfig):
    name = 'games'

   

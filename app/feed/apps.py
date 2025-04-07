from django.apps import AppConfig


class FeedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.feed'

    #def ready(self):
        #from api.tasks import updateFeeds
        #updateFeeds(repeat=60 * 60)  # Démarre la tâche toutes les heures
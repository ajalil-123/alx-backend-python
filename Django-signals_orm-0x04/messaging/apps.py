from django.apps import AppConfig


class MessagingConfig(AppConfig):
    #default_auto_field = 'django.db.models.BigAutoField'
    name = 'messaging'

    
    # Load signals when the app is ready
    def ready(self):
        import messaging.signals  # Importing signals to connect them to model events

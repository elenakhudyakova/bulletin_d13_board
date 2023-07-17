from django.apps import AppConfig

class MMORPG_messagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MMORPG_messages'

    def ready(self):
        import MMORPG_messages.signals

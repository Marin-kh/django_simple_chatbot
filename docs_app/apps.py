from django.apps import AppConfig


class DocsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'docs_app'

    def ready(self):
        import docs_app.signals

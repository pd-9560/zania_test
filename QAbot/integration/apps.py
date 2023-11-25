from django.apps import AppConfig

# an app to store and index data in form of pdfs
class IntegrationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'integration'

from django.apps import AppConfig


class ApiConfig(AppConfig):
    """
    Configuration class for the 'quiz_app' Django application.
    This class defines app-level settings and can be used to register signals, override ready logic, etc.
    """
    # Default type for auto-incrementing primary keys
    default_auto_field = 'django.db.models.BigAutoField'
    
    # App name as it appears in INSTALLED_APPS
    name = 'quiz_app'

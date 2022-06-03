from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"

    def ready(self):
        # TODO: implement more elegant plugin registration & initialization one day
        from app.plugins import init_plugins

        init_plugins()

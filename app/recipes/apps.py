from django.apps import AppConfig


class RecipesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.recipes'

    def ready(self):
        import app.recipes.signals  # Импорт для активации обработчиков сигналов

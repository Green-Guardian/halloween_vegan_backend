from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from app.recipes.models import Recipe
from app.recipes.serializers import RecipeSerializer


@extend_schema_view(
    create=extend_schema(summary="Создать новый рецепт"),
    update=extend_schema(summary="Обновить существующий рецепт"),
    partial_update=extend_schema(summary="Частично обновить рецепт"),
    destroy=extend_schema(summary="Удалить рецепт"),
    list=extend_schema(summary="Получить список рецептов"),
    retrieve=extend_schema(summary="Получить детали рецепта")
)
class RecipeViewSet(viewsets.ModelViewSet):
    """
    API эндпоинт для работы с рецептами.
    Позволяет просматривать, создавать, обновлять и удалять рецепты.
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return super().get_permissions()


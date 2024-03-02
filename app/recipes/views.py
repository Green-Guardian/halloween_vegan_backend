from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from app.recipes.models import Recipe
from app.recipes.serializers import RecipeSerializer

from django.shortcuts import get_object_or_404


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

    def get_serializer_context(self):
        context = super(RecipeViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return super().get_permissions()

    def get_object(self):
        """
        Переопределяет метод для поиска объекта по slug или ID.
        """
        lookup_value = self.kwargs.get(self.lookup_url_kwarg or self.lookup_field)

        if lookup_value.isdigit():
            filter_kwargs = {'id': lookup_value}
        else:
            filter_kwargs = {'slug': lookup_value}

        obj = get_object_or_404(self.queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)

        return obj

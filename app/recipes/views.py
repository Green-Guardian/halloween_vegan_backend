from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

from app.recipes.models import Recipe
from app.recipes.serializers import RecipeSerializer

from django.shortcuts import get_object_or_404


@extend_schema_view(
    create=extend_schema(summary="Создать новый рецепт"),
    update=extend_schema(summary="Обновить существующий рецепт"),
    partial_update=extend_schema(summary="Частично обновить рецепт"),
    destroy=extend_schema(summary="Удалить рецепт"),
    list=extend_schema(summary="Получить список рецептов"),
    retrieve=extend_schema(summary="Получить детали рецепта"),
    winners_all_year=extend_schema(summary="Получить рецепты победителей"),
    winners_by_year=extend_schema(summary="Получить рецепты победителей по конкретному году"),
    recipes_by_year=extend_schema(summary="Получить рецепты по году"),
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

    @action(detail=False, methods=['get'], url_path='winners/year')
    def winners_all_year(self, request):
        """
        Возвращает список победителей для каждого года.
        """
        winners = Recipe.objects.filter(place__isnull=False).order_by('-year', 'place')
        serializer = self.get_serializer(winners, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='winners/year/(?P<year>[0-9]{4})')
    def winners_by_year(self, request, year=None):
        """
        Возвращает список победителей за указанный год.
        """
        winners = self.queryset.filter(year=year).exclude(place__isnull=True).order_by('place')
        serializer = self.get_serializer(winners, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='year/(?P<year>[0-9]{4})')
    def recipes_by_year(self, request, year=None):
        """
        Возвращает список рецептов за указанный год.
        """
        recipes = self.queryset.filter(year=year)
        page = self.paginate_queryset(recipes)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recipes, many=True)
        return Response(serializer.data)

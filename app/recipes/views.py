from rest_framework import viewsets
from app.recipes.models import Recipe
from app.recipes.serializers import RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

from rest_framework import serializers
from app.recipes.models import Recipe, Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)
    slug = serializers.SlugField(required=False)

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

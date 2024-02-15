from rest_framework import serializers
from app.recipes.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(required=False)

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

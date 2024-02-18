from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from rest_framework import serializers
from app.recipes.models import Recipe

from django.utils.timezone import now


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Пример",
            summary="Пример ответа",
            description="Описание примера ответа сериализатора",
            value={
                "id": 206,
                "slug": "zhutko-shokoladnye-zombi-keksy",
                "image": "https://seal-pavel.website/media/recipes/2023/zombi-keksy.png",
                "title": "Жутко шоколадные зомби-кексы",
                "author": "Василий",
                "author_link": "https://t.me/example",
                "description": "Ходят слухи, что если добавить в печеньки с шоколадками разрыхлитель теста, то ...",
                "ingredients": [
                    {
                        "url": "https://veganrussian.ru/pancakes-mix-aladushkin/",
                        "name": "180 гр льняной муки,"
                    },
                    {
                        "name": "..."
                    },
                    {
                        "name": "~ 70 гр кокосового масла."
                    }
                ],
                "tools": [
                    "Тара для замешивания теста,",
                    "...",
                    "Железная рюмка."
                ],
                "steps": [
                    "Смешиваем сахар, льняную муку и разрыхлитель теста.",
                    "...",
                    "Жутко шоколадные зомби-кексы готовы!"
                ],
                "category": "Десерт",
                "year": now().year,
                "internal_comment": "Все верно написано тут?",
                "place": None,
                "published": True,
                "created_at": "2024-02-17T14:58:38.201606+03:00",
                "updated_at": "2024-02-17T14:58:38.201632+03:00"
            },
            request_only=False,  # Применимо только к ответу
            response_only=True,
        ),
    ]
)
class RecipeSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(required=False)

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

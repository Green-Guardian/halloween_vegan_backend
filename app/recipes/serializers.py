from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from rest_framework import serializers
from app.recipes.models import Recipe
from django.utils.timezone import now
from easy_thumbnails.files import get_thumbnailer


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
    slug = serializers.SlugField(required=False)  # Для поиска по slug
    image_big = serializers.SerializerMethodField()
    image_small = serializers.SerializerMethodField()
    image_thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

    def get_image_big(self, obj):
        request = self.context.get('request')
        if obj.image:
            options = {'size': (1500, 1500), 'crop': False}
            thumbnailer = get_thumbnailer(obj.image)
            thumbnail = thumbnailer.get_thumbnail(options)
            return request.build_absolute_uri(thumbnail.url)
        return None

    def get_image_small(self, obj):
        request = self.context.get('request')
        if obj.image:
            options = {'size': (500, 500), 'crop': False}
            thumbnailer = get_thumbnailer(obj.image)
            thumbnail = thumbnailer.get_thumbnail(options)
            return request.build_absolute_uri(thumbnail.url)
        return None

    def get_image_thumbnail(self, obj):
        request = self.context.get('request')
        if obj.image:
            options = {'size': (100, 100), 'crop': False}
            thumbnailer = get_thumbnailer(obj.image)
            thumbnail = thumbnailer.get_thumbnail(options)
            return request.build_absolute_uri(thumbnail.url)
        return None

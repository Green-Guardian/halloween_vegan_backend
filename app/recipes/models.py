from pathlib import Path

from django.db import models
from django.utils.timezone import now

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit

from autoslug import AutoSlugField
from uuslug import slugify as uuslug_slugify


# Для авто-миграций
def custom_slugify(text, *args, **kwargs):
    return uuslug_slugify(text, *args, **kwargs)


def upload_to_directory(instance, filename):
    current_year = now().year
    extension = Path(filename).suffix
    new_filename = f"{instance.slug}_original{extension}"
    return f'recipes/{current_year}/{new_filename}'


class Recipe(models.Model):
    image = models.ImageField(upload_to=upload_to_directory)
    image_average = ImageSpecField(source='image',
                                   processors=[ResizeToFit(1500, 1500, False)],
                                   format='WEBP',
                                   options={'quality': 90})
    image_small = ImageSpecField(source='image',
                                 processors=[ResizeToFit(500, 500, False)],
                                 format='WEBP',
                                 options={'quality': 90})

    title = models.CharField(max_length=200, unique=True)
    author = models.CharField(max_length=100)
    author_link = models.URLField(blank=True)
    description = models.TextField(blank=True)
    ingredients = models.JSONField(default=list)
    tools = models.JSONField(default=list)
    steps = models.JSONField(default=list)

    category = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    internal_comment = models.TextField(null=True, blank=True)
    place = models.IntegerField(blank=True, null=True)
    published = models.BooleanField(default=False, db_index=True)

    slug = AutoSlugField(populate_from='title', unique=True, slugify=custom_slugify, always_update=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'recipes'
        permissions = [
            ("can_choose_winners", "Может выбрать победителей"),
            ("can_publish", "Может публиковать рецепты"),
            ("can_unpublish", "Может снимать рецепты с публикации"),
        ]

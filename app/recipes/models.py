from django.db import models
from django.utils.timezone import now

from autoslug import AutoSlugField
from uuslug import slugify as uuslug_slugify


def custom_slugify(text, *args, **kwargs):
    return uuslug_slugify(text, *args, **kwargs)


class Ingredient(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'recipes'


class Recipe(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = AutoSlugField(populate_from='title', unique=True, slugify=custom_slugify, always_update=True)
    image = models.ImageField(upload_to='recipes/')
    author = models.CharField(max_length=100)
    author_link = models.URLField(blank=True)
    year = models.PositiveIntegerField(default=now().year)
    description = models.TextField()
    category = models.CharField(max_length=100)
    tools = models.TextField()
    steps = models.TextField()
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    place = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'recipes'

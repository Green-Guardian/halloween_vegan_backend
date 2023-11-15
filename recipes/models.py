from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.quantity} of {self.name}"


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    prep_time = models.PositiveIntegerField(help_text="Preparation time in minutes")
    steps = models.TextField(help_text="Step by step instructions")
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes')

    def __str__(self):
        return self.title

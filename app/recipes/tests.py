from app.halloween_vegan_backend import settings
from app.recipes.models import Recipe, Ingredient

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class RecipeTests(APITestCase):
    def test_create_recipe(self):
        """
        Ensure we can create a new recipe object.
        """
        url = reverse('recipe-list')

        Ingredient.objects.create(name='Sugar')
        sugar = Ingredient.objects.get(name='Sugar')

        # image_path = settings.MEDIA_ROOT / 'recipes' / 'for_tests.jpg'
        image_path = 'for_tests.jpg'
        with open(image_path, 'rb') as img_file:
            image_content = img_file.read()
        assert image_content, f"File is empty or couldn't be read: {image_path}"

        image = SimpleUploadedFile(name='for_tests.jpg', content=image_content, content_type='image/jpeg')

        data = {
            'title': 'Test Recipe',
            'image': image,
            'author': 'Test Author',
            'year': 2021,
            'description': 'This is a test description.',
            'category': 'Test Category',
            'tools': 'Test Tool 1, Test Tool 2',
            'steps': 'Step 1, Step 2',
            'ingredients': [sugar.id],
        }

        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Recipe.objects.count(), 1)
        self.assertEqual(Recipe.objects.get().title, 'Test Recipe')

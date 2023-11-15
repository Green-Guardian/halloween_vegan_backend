from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Recipe


class RecipeTests(APITestCase):
    def test_create_recipe(self):
        """
        Ensure we can create a new recipe object.
        """
        url = reverse('recipe-list')
        data = {'title': 'Test Recipe', 'description': 'This is a test description.'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Recipe.objects.count(), 1)
        self.assertEqual(Recipe.objects.get().title, 'Test Recipe')

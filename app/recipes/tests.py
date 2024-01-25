# from app.halloween_vegan_backend import settings
# from app.recipes.models import Recipe, Ingredient
#
# from django.core.files.uploadedfile import SimpleUploadedFile
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
#
# image_path = settings.MEDIA_ROOT / 'recipes' / 'for_tests.jpg'
# with open(image_path, 'rb') as img_file:
#     image_content = img_file.read()
# assert image_content, f"File is empty or couldn't be read: {image_path}"
#
# image = SimpleUploadedFile(name='for_tests.jpg', content=image_content, content_type='image/jpeg')
#
#
# class RecipeTests(APITestCase):
#     def test_create_recipe(self):
#         """
#         Ensure we can create a new recipe object.
#         """
#         url = reverse('recipe-list')
#
#         Ingredient.objects.create(name='Sugar')
#         sugar = Ingredient.objects.get(name='Sugar')
#
#         data = {
#             'title': 'Test Recipe',
#             'image': image,
#             'author': 'Test Author',
#             'year': 2021,
#             'description': 'This is a test description.',
#             'category': 'Test Category',
#             'tools': 'Test Tool 1, Test Tool 2',
#             'steps': 'Step 1, Step 2',
#             'ingredients': [sugar.id],
#         }
#
#         response = self.client.post(url, data, format='multipart')
#         print(response.data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Recipe.objects.count(), 1)
#         self.assertEqual(Recipe.objects.get().title, 'Test Recipe')
#
#     def test_update_recipe(self):
#         """
#         Ensure we can update a recipe object.
#         """
#         recipe = Recipe.objects.create(
#             title='Test Recipe',
#             image=image,
#             author='Test Author',
#             year=2021,
#             description='This is a test description.',
#             category='Test Category',
#             tools='Test Tool 1, Test Tool 2',
#             steps='Step 1, Step 2',
#         )
#
#         url = reverse('recipe-detail', args=[recipe.id])
#
#         data = {
#             'title': 'Updated Recipe',
#             'author': 'Updated Author',
#         }
#
#         response = self.client.patch(url, data)
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['title'], 'Updated Recipe')
#         self.assertEqual(response.data['author'], 'Updated Author')
#
#     def test_retrieve_recipe(self):
#         """
#         Ensure we can retrieve a recipe object.
#         """
#         recipe = Recipe.objects.create(
#             title='Test Recipe',
#             image=image,
#             author='Test Author',
#             year=2021,
#             description='This is a test description.',
#             category='Test Category',
#             tools='Test Tool 1, Test Tool 2',
#             steps='Step 1, Step 2',
#         )
#
#         url = reverse('recipe-detail', args=[recipe.id])
#         response = self.client.get(url)
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['title'], 'Test Recipe')
#
#     def test_delete_recipe(self):
#         """
#         Ensure we can delete a recipe object.
#         """
#         recipe = Recipe.objects.create(
#             title='Test Recipe',
#             image=image,
#             author='Test Author',
#             year=2021,
#             description='This is a test description.',
#             category='Test Category',
#             tools='Test Tool 1, Test Tool 2',
#             steps='Step 1, Step 2',
#         )
#
#         url = reverse('recipe-detail', args=[recipe.id])
#         response = self.client.delete(url)
#
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(Recipe.objects.count(), 0)
#
#     def test_list_recipes(self):
#         """
#         Ensure we can retrieve a list of all recipe objects.
#         """
#         Recipe.objects.create(
#             title='Test Recipe 1',
#             image=image,
#             author='Test Author',
#             year=2021,
#             description='This is a test description.',
#             category='Test Category',
#             tools='Test Tool 1, Test Tool 2',
#             steps='Step 1, Step 2',
#         )
#         Recipe.objects.create(
#             title='Test Recipe 2',
#             image=image,
#             author='Test Author',
#             year=2021,
#             description='This is a test description.',
#             category='Test Category',
#             tools='Test Tool 1, Test Tool 2',
#             steps='Step 1, Step 2',
#         )
#
#         url = reverse('recipe-list')
#         response = self.client.get(url)
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 2)
#
#     def test_create_recipe_without_title(self):
#         """
#         Ensure we get an error when creating a recipe without a title.
#         """
#         url = reverse('recipe-list')
#
#         Ingredient.objects.create(name='Sugar')
#         sugar = Ingredient.objects.get(name='Sugar')
#
#         data = {
#             'image': image,
#             'author': 'Test Author',
#             'year': 2021,
#             'description': 'This is a test description.',
#             'category': 'Test Category',
#             'tools': 'Test Tool 1, Test Tool 2',
#             'steps': 'Step 1, Step 2',
#             'ingredients': [sugar.id],
#         }
#
#         response = self.client.post(url, data, format='multipart')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(Recipe.objects.count(), 0)

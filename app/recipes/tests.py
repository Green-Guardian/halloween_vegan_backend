import tempfile
import shutil

from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.test import TestCase, RequestFactory
from django.db.utils import IntegrityError
from django.utils.timezone import now
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User, Permission
from django.contrib.messages.storage.fallback import FallbackStorage

from app.recipes.admin import RecipeAdmin, publish_recipes, unpublish_recipes

from .models import Recipe
from .forms import RecipeForm


class RecipeAdminTest(TestCase):
    jpeg_image = (
        b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H'
        b'\x00\x00\xff\xdb\x00C\x00\x03\x02\x02\x02\x02\x02\x03\x02'
        b'\x02\x02\x03\x03\x03\x03\x04\x06\x04\x04\x04\x04\x04\x08\x06'
        b'\x06\x05\x06\t\x08\n\n\t\x08\t\t\n\x0c\x0f\x0c\n\x0b\x0e\x0b'
        b'\t\t\r\x11\r\x0e\x0f\x10\x10\x11\x10\n\x0c\x12\x13\x12\x10\x13'
        b'\x0f\x10\x10\x10\xff\xc9\x00\x0b\x08\x00\x01\x00\x01\x01\x01'
        b'\x11\x00\xff\xcc\x00\x06\x00\x10\x10\x05\xff\xda\x00\x08\x01'
        b'\x01\x00\x00?\x00\xd2\xcf \xff\xd9'
    )

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаем временную директорию для медиафайлов
        cls.temp_media_dir = tempfile.mkdtemp()
        # Переопределяем MEDIA_ROOT, чтобы указывать на временную директорию
        settings.MEDIA_ROOT = cls.temp_media_dir

    @classmethod
    def tearDownClass(cls):
        # Удаляем временную директорию после завершения всех тестов
        shutil.rmtree(cls.temp_media_dir, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.site = AdminSite()
        self.factory = RequestFactory()
        self.image_file = SimpleUploadedFile(name='test_image.jpg', content=self.jpeg_image, content_type='image/jpeg')
        self.superuser = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='password'
        )
        self.user = User.objects.create_user(
            username='testuser', email='user@example.com', password='password'
        )
        # Назначаем пользователю разрешение на публикацию рецептов
        publish_permission = Permission.objects.get(codename='can_publish')
        self.user.user_permissions.add(publish_permission)
        # Назначаем пользователю разрешение на снятие рецептов с публикации
        unpublish_permission = Permission.objects.get(codename='can_unpublish')
        self.user.user_permissions.add(unpublish_permission)
        # Создание тестового рецепта
        self.recipe = Recipe.objects.create(
            title="Test Recipe",
            author="Test Author",
            author_link="https://example.com",
            description="Test Description",
            ingredients=[{"name": "Test Ingredient", "url": "https://example.com"}],
            tools=["Test Tool 1", "Test Tool 2"],
            steps=["Test Step 1", "Test Step 2"],
            category="Test Category",
            year=now().year,
            image=self.image_file
        )

    def test_publish_recipes_action(self):
        # Создание объекта запроса
        request = self.factory.get('/admin/app/recipe/')
        request.user = self.user

        # Добавление поддержки сообщений к запросу
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        # Получение queryset с тестовым рецептом
        queryset = Recipe.objects.all()

        # Вызов функции действия напрямую
        publish_recipes(RecipeAdmin(Recipe, self.site), request, queryset)

        # Проверка, что рецепт был опубликован
        self.recipe.refresh_from_db()
        self.assertTrue(self.recipe.published)

        # Проверка наличия сообщения об успешной публикации
        self.assertEqual(len(messages._queued_messages), 1)

    def test_unpublish_recipes_action(self):
        request = self.factory.get('/admin/app/recipe/')
        request.user = self.superuser

        # Добавляем поддержку сообщений в запрос
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        # Получаем QuerySet с одним рецептом
        queryset = Recipe.objects.filter(id=self.recipe.id)

        unpublish_recipes(RecipeAdmin(Recipe, self.site), request, queryset)

        self.recipe.refresh_from_db()  # Обновляем объект из базы данных
        self.assertFalse(self.recipe.published)
        self.assertEqual(len(messages._queued_messages), 1)

    def test_get_fieldsets_with_permissions(self):
        request = self.factory.get('/admin/app/recipe/add/')
        request.user = self.superuser

        ma = RecipeAdmin(Recipe, self.site)
        fieldsets = ma.get_fieldsets(request)

        # Проверяем, что для суперпользователя доступен расширенный набор fieldsets
        self.assertTrue(any('Admin' in fs[0] for fs in fieldsets))


class RecipeModelTest(TestCase):
    jpeg_image = (
        b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H'
        b'\x00\x00\xff\xdb\x00C\x00\x03\x02\x02\x02\x02\x02\x03\x02'
        b'\x02\x02\x03\x03\x03\x03\x04\x06\x04\x04\x04\x04\x04\x08\x06'
        b'\x06\x05\x06\t\x08\n\n\t\x08\t\t\n\x0c\x0f\x0c\n\x0b\x0e\x0b'
        b'\t\t\r\x11\r\x0e\x0f\x10\x10\x11\x10\n\x0c\x12\x13\x12\x10\x13'
        b'\x0f\x10\x10\x10\xff\xc9\x00\x0b\x08\x00\x01\x00\x01\x01\x01'
        b'\x11\x00\xff\xcc\x00\x06\x00\x10\x10\x05\xff\xda\x00\x08\x01'
        b'\x01\x00\x00?\x00\xd2\xcf \xff\xd9'
    )

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаем временную директорию для медиафайлов
        cls.temp_media_dir = tempfile.mkdtemp()
        # Переопределяем MEDIA_ROOT, чтобы указывать на временную директорию
        settings.MEDIA_ROOT = cls.temp_media_dir

    @classmethod
    def tearDownClass(cls):
        # Удаляем временную директорию после завершения всех тестов
        shutil.rmtree(cls.temp_media_dir, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.form_data = {
            'title': 'Test Recipe',
            'author': 'Test Author',
            'category': 'Test Category',
            'year': now().year,
            'description': 'Test Description',
            'tools': 'Spoon,\nBowl.',
            'steps': 'Mix ingredients.\nBake for 20 minutes!',
            'ingredients': 'Flour 1kg\nSugar 200g https://example.com/sugar'
        }
        self.image_file = SimpleUploadedFile(name='test_image.jpg', content=self.jpeg_image, content_type='image/jpeg')

    def test_create_recipe_with_image(self):
        # Создаем тестовое изображение
        image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')

        # Создаем экземпляр модели Recipe с тестовым изображением
        recipe = Recipe.objects.create(
            title="Test Recipe",
            author="Test Author",
            author_link="https://example.com",
            description="Test Description",
            ingredients=[{"name": "Test Ingredient", "url": "https://example.com"}],
            tools=["Test Tool 1", "Test Tool 2"],
            steps=["Test Step 1", "Test Step 2"],
            category="Test Category",
            year=now().year,
            image=image
        )

        # Проверяем, был ли рецепт успешно создан и содержит ли он изображение
        self.assertTrue(isinstance(recipe, Recipe))
        self.assertEqual(recipe.title, "Test Recipe")
        self.assertTrue(recipe.image, 'test_image.jpg')

    def test_title_uniqueness(self):
        Recipe.objects.create(
            title="Unique Recipe",
            author="Author",
            category="Category",
            year=now().year,
            image=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        )

        with self.assertRaises(IntegrityError):
            Recipe.objects.create(
                title="Unique Recipe",  # Такое же название, как у первого рецепта
                author="Another Author",
                category="Another Category",
                year=now().year,
                image=SimpleUploadedFile(name='another_test_image.jpg', content=b'', content_type='image/jpeg')
            )

    def test_recipe_published_status(self):
        recipe = Recipe.objects.create(
            title="Test Publish",
            author="Author",
            category="Category",
            year=now().year,
            published=True,  # Рецепт опубликован
            image=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        )

        self.assertTrue(recipe.published)

    def test_auto_slug_generation(self):
        recipe = Recipe.objects.create(
            title="Recipe for Slug Testing",
            author="Author",
            category="Category",
            year=now().year,
            image=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        )

        self.assertEqual(recipe.slug, "recipe-for-slug-testing")

    def test_str_representation(self):
        recipe = Recipe.objects.create(
            title="Str Method Test",
            author="Author",
            category="Category",
            year=now().year,
            image=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        )

        self.assertEqual(str(recipe), "Str Method Test")

    def test_form_with_all_required_fields(self):
        image_file = SimpleUploadedFile(name='test_image.jpg', content=self.jpeg_image, content_type='image/jpeg')

        form_data = {
            'title': 'Test Recipe',
            'author': 'Test Author',
            'category': 'Test Category',
            'year': now().year,
            'description': 'Test Description',
            'tools': 'Spoon\nBowl',
            'steps': 'Mix ingredients\nBake for 20 minutes',
            'ingredients': 'Flour 1kg\nSugar 200g https://example.com/sugar'
        }

        form = RecipeForm(data=form_data, files={'image': image_file})
        self.assertTrue(form.is_valid(), form.errors.as_text())

    def test_form_with_invalid_data(self):
        # Пустое содержимое для обязательного поля 'title'
        form_data = self.form_data.copy()
        form_data['title'] = ''
        form = RecipeForm(data=form_data, files={'image': self.image_file})
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

        # Невалидный год
        form_data = self.form_data.copy()
        form_data['year'] = 'notayear'
        form = RecipeForm(data=form_data, files={'image': self.image_file})
        self.assertFalse(form.is_valid())
        self.assertIn('year', form.errors)

        # Проверка на отсутствие обязательного изображения
        form_data = self.form_data.copy()
        form = RecipeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('image', form.errors)

    def test_form_saves_correctly(self):
        form_data = self.form_data.copy()
        form = RecipeForm(data=form_data, files={'image': self.image_file})
        self.assertTrue(form.is_valid())
        recipe = form.save()
        self.assertIsNotNone(recipe.pk)  # Убедимся, что рецепт был сохранен и имеет первичный ключ
        self.assertEqual(recipe.title, form_data['title'])
        self.assertEqual(recipe.author, form_data['author'])

    def test_form_with_missing_data(self):
        # Отсутствует title
        missing_title_data = self.form_data.copy()
        del missing_title_data['title']
        form_missing_title = RecipeForm(data=missing_title_data, files={'image': self.image_file})
        self.assertFalse(form_missing_title.is_valid())
        self.assertIn('title', form_missing_title.errors)

        # Отсутствует author
        missing_author_data = self.form_data.copy()
        del missing_author_data['author']
        form_missing_author = RecipeForm(data=missing_author_data, files={'image': self.image_file})
        self.assertFalse(form_missing_author.is_valid())
        self.assertIn('author', form_missing_author.errors)

        # Отсутствует category
        missing_category_data = self.form_data.copy()
        del missing_category_data['category']
        form_missing_category = RecipeForm(data=missing_category_data, files={'image': self.image_file})
        self.assertFalse(form_missing_category.is_valid())
        self.assertIn('category', form_missing_category.errors)

        # Отсутствует year
        missing_year_data = self.form_data.copy()
        del missing_year_data['year']
        form_missing_year = RecipeForm(data=missing_year_data, files={'image': self.image_file})
        self.assertFalse(form_missing_year.is_valid())
        self.assertIn('year', form_missing_year.errors)

    def test_ingredients_url_validation(self):
        # Валидный URL
        valid_url_data = self.form_data.copy()
        valid_url_data['ingredients'] = "Flour 1kg\nSugar 200g https://example.com/sugar"
        form_valid_url = RecipeForm(data=valid_url_data, files={'image': self.image_file})
        self.assertTrue(form_valid_url.is_valid())

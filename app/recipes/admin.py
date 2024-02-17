from django.contrib import admin, messages
from django.utils.html import format_html
from django.utils.timezone import now

from app.recipes.models import Recipe
from app.recipes.forms import RecipeForm


def publish_recipes(modeladmin, request, queryset):
    if not request.user.has_perm('recipes.can_publish'):
        modeladmin.message_user(request, "У вас нет прав на публикацию рецептов.", level=messages.ERROR)
        return
    queryset.update(published=True)
    modeladmin.message_user(request, "Выбранные рецепты были опубликованы.")


def unpublish_recipes(modeladmin, request, queryset):
    if not request.user.has_perm('recipes.can_unpublish'):
        modeladmin.message_user(request, "У вас нет прав на снятие рецептов с публикации.", level=messages.ERROR)
        return
    queryset.update(published=False)
    modeladmin.message_user(request, "Выбранные рецепты были сняты с публикации.")


publish_recipes.short_description = "Publish selected recipes"
unpublish_recipes.short_description = "Unpublish selected recipes"


class RecipeAdmin(admin.ModelAdmin):
    form = RecipeForm
    search_fields = ('title', 'description')
    list_filter = ('published', 'category', 'year', 'place',)
    list_display = ('title', 'published', 'image_thumbnail')
    readonly_fields = ('image_thumbnail',)
    actions = (publish_recipes, unpublish_recipes)
    base_fieldsets = (
        ('Participant', {
            'fields': ('author', 'author_link',)
        }),
        ('Recipe', {
            'fields': (
            'image_thumbnail', 'image', 'title', 'description', 'ingredients', 'tools', 'steps', 'category', 'year',)
        }),
        ('Other', {
            'fields': ('internal_comment',)
        }),
    )

    # Отображение фото рецепта в админке
    def image_thumbnail(self, obj=None):
        if obj and obj.image:
            return format_html('<img src="{}" style="width: 75px; height:auto;" />', obj.image.url)
        return "-"

    image_thumbnail.short_description = 'Image Preview'

    # Динамическое изменение fieldsets в зависимости от разрешений пользователя
    def get_fieldsets(self, request, obj=None):
        fieldsets = list(self.base_fieldsets)  # Копируем базовую конфигурацию
        admin_fields = []

        if request.user.has_perm('recipes.can_choose_winners'):
            admin_fields.append('place')
        if request.user.has_perm('recipes.can_publish'):
            admin_fields.append('published')

        if admin_fields:
            fieldsets.append(('Admin', {'fields': admin_fields}))

        return fieldsets

    def get_changeform_initial_data(self, request):
        initial = super(RecipeAdmin, self).get_changeform_initial_data(request)
        initial['year'] = now().year
        return initial


admin.site.register(Recipe, RecipeAdmin)

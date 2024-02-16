from django.contrib import admin, messages
from django.utils.html import format_html

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
    fieldsets = (
        ('Participant', {
            'fields': ('author', 'author_link',)
        }),
        ('Recipe', {
            'fields': ('image_thumbnail', 'image', 'title', 'description', 'ingredients', 'tools', 'steps',)
        }),
        ('Other', {
            'fields': ('category', 'year',)
        }),
    )

    # Отображение фото рецепта в админке
    def image_thumbnail(self, obj=None):
        if obj and obj.image:
            return format_html('<img src="{}" style="width: 75px; height:auto;" />', obj.image.url)
        return "-"

    image_thumbnail.short_description = 'Image Preview'

    # Отображение полей рецепта в зависимости от разрешений пользователя
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        modified_fieldsets = []

        for name, options in fieldsets:
            fields = list(options["fields"])

            if name == 'Other':
                if request.user.has_perm('recipes.can_choose_winners') and 'place' not in fields:
                    fields.append('place')
                if request.user.has_perm('recipes.can_publish') and 'published' not in fields:
                    fields.append('published')

            modified_fieldsets.append((name, {'fields': fields}))

        return modified_fieldsets


admin.site.register(Recipe, RecipeAdmin)

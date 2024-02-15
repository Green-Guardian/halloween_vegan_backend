from django.contrib import admin
from django.utils.html import format_html

from app.recipes.models import Recipe
from app.recipes.forms import RecipeForm

privileged_groups = [group.lower() for group in
                     ('main', 'seal', 'admin',)]
sensitive_fields = ('place', 'is_active',)


def publish_recipes(modeladmin, request, queryset):
    queryset.update(is_active=True)


def unpublish_recipes(modeladmin, request, queryset):
    queryset.update(is_active=False)


publish_recipes.short_description = "Publish selected recipes"
unpublish_recipes.short_description = "Unpublish selected recipes"


class RecipeAdmin(admin.ModelAdmin):
    form = RecipeForm
    search_fields = ('title', 'description')
    list_filter = ('is_active', 'category', 'year', 'place',)
    list_display = ('title', 'is_active', 'image_thumbnail')
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
            'fields': ('category', 'year', 'place', 'is_active',)
        }),
    )

    def image_thumbnail(self, obj=None):
        if obj and obj.image:
            return format_html('<img src="{}" style="width: 75px; height:auto;" />', obj.image.url)
        return "-"

    image_thumbnail.short_description = 'Image Preview'

    def get_form(self, request, obj=None, **kwargs):
        user_groups = [group.lower() for group in request.user.groups.values_list('name', flat=True)]

        if not any(group in user_groups for group in privileged_groups):
            self.exclude = sensitive_fields
        else:
            self.exclude = ()

        return super(RecipeAdmin, self).get_form(request, obj, **kwargs)


admin.site.register(Recipe, RecipeAdmin)

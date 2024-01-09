from django.contrib import admin
from app.recipes.models import Recipe, Ingredient

privileged_groups = ('main', 'seal', 'admin',)
sensitive_fields = ('place', 'is_active',)


class RecipeAdmin(admin.ModelAdmin):
    search_fields = ('title', 'description')
    list_filter = ('is_active', 'category', 'year', 'place',)

    filter_horizontal = ('ingredients',)

    def get_form(self, request, obj=None, **kwargs):
        user_groups = [group.lower() for group in request.user.groups.values_list('name', flat=True)]

        if not any(group in user_groups for group in privileged_groups):
            self.exclude = sensitive_fields
        else:
            self.exclude = ()

        return super(RecipeAdmin, self).get_form(request, obj, **kwargs)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)

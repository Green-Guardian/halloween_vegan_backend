from django.contrib import admin
from app.recipes.models import Recipe, Ingredient


class RecipeAdmin(admin.ModelAdmin):
    search_fields = ('title', 'description')
    list_filter = ('is_active', 'category', 'year', 'place',)

    filter_horizontal = ('ingredients',)

    def get_form(self, request, obj=None, **kwargs):
        if request.user.groups.filter(name='Posting').exists():
            self.exclude = ('place', 'is_active',)

        elif request.user.groups.filter(name='Main').exists():
            self.exclude = ()

        return super(RecipeAdmin, self).get_form(request, obj, **kwargs)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)

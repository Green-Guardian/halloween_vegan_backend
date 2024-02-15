from django import forms
from .models import Recipe


class RecipeForm(forms.ModelForm):
    tools = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 7, 'cols': 85}),
        help_text="Каждый элемент с новой строки.")
    steps = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 7, 'cols': 85}),
        help_text="Каждый элемент с новой строки.")
    ingredients = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 7, 'cols': 85}),
        help_text="Каждый элемент с новой строки (в конце можно добавить ссылку в полном формате, с https://).")

    class Meta:
        model = Recipe
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.tools:
            self.initial['tools'] = "\n".join(self.instance.tools)

        if self.instance and self.instance.steps:
            self.initial['steps'] = "\n".join(self.instance.steps)

        if self.instance and self.instance.ingredients:
            self.initial['ingredients'] = "\n".join([f"{ing['name']}"
                                                     + (f" {ing['url']}" if 'url' in ing else '')
                                                     for ing in self.instance.ingredients])

    def clean_tools(self):
        tools = self.cleaned_data['tools']
        tools_list = [tool.strip() for tool in tools.splitlines() if tool.strip()]
        return tools_list

    def clean_steps(self):
        steps = self.cleaned_data['steps']
        steps_list = [step.strip() for step in steps.splitlines() if step.strip()]
        return steps_list

    def clean_ingredients(self):
        ingredients_str = self.cleaned_data['ingredients']
        ingredients_list = []
        for line in ingredients_str.splitlines():
            parts = line.split(' http')
            ingredient = {"name": parts[0]}
            if len(parts) == 2:
                ingredient["url"] = 'http' + parts[1]
            ingredients_list.append(ingredient)
        return ingredients_list

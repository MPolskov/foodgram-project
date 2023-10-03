from django.contrib import admin

from .models import (
    Favourites,
    Ingredient,
    IngredientInRecipe,
    Recipe,
    ShoppingCart,
    Tag
)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author'
    )
    readonly_fields = ('in_favorites',)
    list_filter = ('author', 'name', 'tags')

    @admin.display(description='Добавлено в избранное')
    def in_favorites(self, obj):
        return obj.favorite.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)


admin.site.register(Tag)
admin.site.register(IngredientInRecipe)
admin.site.register(Favourites)
admin.site.register(ShoppingCart)

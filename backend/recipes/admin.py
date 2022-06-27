from django.contrib import admin
from django.db.models import Count, Sum

from foodgram.settings import EMPTY_VALUE_DISPLAY
from recipes.models import (AmountOfIngredient, Favorite, Ingredient, Recipe,
                            ShoppingCart, Tag)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug',
        'color'
    )
    list_editable = ('name', 'slug', 'color',)
    search_fields = ('id', 'name', 'slug',)
    list_filter = ('name', 'slug',)
    empty_value_display = EMPTY_VALUE_DISPLAY


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit'
    )
    list_editable = ('name', 'measurement_unit')
    search_fields = ('id', 'name', 'measurement_unit',)
    list_filter = ('name', 'measurement_unit',)
    empty_value_display = EMPTY_VALUE_DISPLAY


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'author', 'name', 'image',
        'text', 'cooking_time',
    )
    list_filter = ('name', 'author', 'tags',)
    readonly_fields = ('added_in_favorites',)
    empty_value_display = EMPTY_VALUE_DISPLAY

    @admin.display(description='Общее число добавлений в избранное')
    def added_in_favorites(self, obj):
        return obj.favorites.count()


@admin.register(AmountOfIngredient)
class AmountOfIngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'ingredient', 'amount', 'get_measurement_unit',
        'get_recipes_count',
    )
    readonly_fields = ('get_measurement_unit',)
    list_filter = ('ingredient',)
    ordering = ('ingredient',)
    empty_value_display = EMPTY_VALUE_DISPLAY

    @admin.display(description='Единица измерения')
    def get_measurement_unit(self, obj):
        try:
            return obj.ingredient.measurement_unit
        except AmountOfIngredient.ingredient.RelatedObjectDoesNotExist:
            return EMPTY_VALUE_DISPLAY

    @admin.display(description='Количество ссылок в рецептах')
    def get_recipes_count(self, obj):
        return obj.recipes.count()


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'count_ingredients',)
    readonly_fields = ('count_ingredients',)
    empty_value_display = EMPTY_VALUE_DISPLAY

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    @admin.display(description='Количество ингредиентов')
    def count_ingredients(self, obj):
        return (
            obj.recipes.all().annotate(count_ingredients=Count('ingredients'))
            .aggregate(total=Sum('count_ingredients'))['total']
        )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    list_filter = ('user', 'recipe',)
    empty_value_display = EMPTY_VALUE_DISPLAY

import django_filters
from django.db.models import IntegerField, Value

from .models import Ingredient, Recipe, ShoppingCart, Tag, User


class IngredientSearchFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='search_by_name')

    class Meta:
        model = Ingredient
        fields = ('name',)

    def search_by_name(self, queryset, name, value):
        if not value:
            return queryset
        start_with_queryset = (
            queryset.filter(name__istartswith=value).annotate(
                order=Value(0, IntegerField())
            )
        )
        contain_queryset = (
            queryset.filter(name__icontains=value).exclude(
                pk__in=(ingredient.pk for ingredient in start_with_queryset)
            ).annotate(
                order=Value(1, IntegerField())
            )
        )
        return start_with_queryset.union(contain_queryset).order_by('order')


class RecipeFilter(django_filters.FilterSet):
    IN = 1
    OUT = 0
    CHOICES = (
        (IN, 1),
        (OUT, 0),
    )
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug'
    )
    author = django_filters.ModelChoiceFilter(
        queryset=User.objects.all()
    )
    is_favorited = django_filters.ChoiceFilter(
        method='get_is_favorited',
        choices=CHOICES
    )
    is_in_shopping_cart = django_filters.BooleanFilter(
        method='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author')

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(favorites__user=user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if not value:
            return queryset
        try:
            recipes = (
                self.request.user.shopping_cart.recipes.all()
            )
        except ShoppingCart.DoesNotExist:
            return queryset
        return queryset.filter(
            pk__in=(recipe.pk for recipe in recipes)
        )

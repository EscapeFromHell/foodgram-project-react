from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter

from .views import (IngredientViewSet, RecipeViewSet, ShoppingCartViewSet,
                    TagViewSet)

app_name = 'recipes'

router_v1 = DefaultRouter()
router_v1.register(r'ingredients', IngredientViewSet, basename='ingredients')
router_v1.register(r'tags', TagViewSet, basename='tags')
router_v1.register(r'recipes', ShoppingCartViewSet, basename='shopping_cart')
router_v1.register(r'recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router_v1.urls)),
]

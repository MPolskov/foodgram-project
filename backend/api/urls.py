from django.urls import path, include
from rest_framework import routers

from .views import (
    IngredientsViewSet,
    TagsViewSet,
    RecipeViewSet,
)

app_name = 'api'


router = routers.DefaultRouter()
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router.register(r'tags', TagsViewSet)
router.register(r'recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
]

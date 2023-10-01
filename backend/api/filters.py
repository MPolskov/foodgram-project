from django_filters.rest_framework import (
    FilterSet,
    filters
)
from recipes.models import Recipe, Tag


class RecipeFilterSet(FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    author = filters.NumberFilter(
        field_name='author',
        lookup_expr='exact'
    )
    is_favorited = filters.BooleanFilter(
        method='filter_is_favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author',)

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if not user.is_anonymous and value:
            recipes = user.subscriber.values('recipe')
            return queryset.filter(id__in=recipes)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if not user.is_anonymous and value:
            recipes = user.buyer.values('recipe')
            return queryset.filter(id__in=recipes)
        return queryset

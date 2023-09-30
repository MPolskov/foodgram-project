from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny, SAFE_METHODS
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import action

from recipes.models import (
    Ingredient,
    Tag,
    Recipe,
    Favourites,
)
from .serializers import (
    IngredientsSerializer,
    TagsSerializer,
    RecipeReadSerializer,
    RecipeWriteSerializer,
    RecipeInFavoriteSerializer,

)


class IngredientsViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = IngredientsSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)


class TagsViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TagsSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination

    # def get_queryset(self):
    #     queryset = Recipe.objects.all()
    #     user = self.request.user
    #     if self.kwargs.get('is_favorited') == 1:
    #         queryset = user.favorite.all()
    #     return queryset
    
    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer
    
    @action(
        methods=['post', 'delete'],
        detail=True,
        # permission_classes=[permissions.IsAuthenticated]
    )
    def favorite(self, request, pk):
        user = request.user
        if request.method == 'POST':
            if user.subscriber.filter(favorite=pk).exists():
                return Response(
                    {'errors': 'Рецепт уже добавлен в избранное!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            recipe = get_object_or_404(Recipe, id=pk)
            subscription = Favourites.objects.create(
                user=user,
                favorite=recipe
            )
            serializer = RecipeInFavoriteSerializer(subscription)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        recipe = user.subscriber.filter(favorite=pk)
        if recipe:
            recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {'errors': 'В избранном такого рецепта нет!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        


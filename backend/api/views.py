from django.shortcuts import get_object_or_404

from rest_framework import mixins
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination

from recipes.models import (
    Ingredient,
    Tag,
    Recipe,
)
from .serializers import (
    IngredientsSerializer,
    TagsSerializer,
    RecipeSerializer,

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
    # queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        queryset = Recipe.objects.all()
        user = self.request.user
        if self.kwargs.get('is_favorited') == 1:
            queryset = user.subscriber.all()
        return queryset
    #     review_id = self.kwargs.get('review_id')
    #     title_id = self.kwargs.get('title_id')
    #     review = get_object_or_404(Review, id=review_id, title=title_id)
    #     return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        # title_id = self.kwargs.get('title_id')
        # review_id = self.kwargs.get('review_id')
        # review = get_object_or_404(Review, id=review_id, title=title_id)
        # serializer.save(author=self.request.user, review=review)
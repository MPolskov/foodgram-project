from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from .filters import RecipeFilterSet
from .errors_msg import (
    ERROR_MSG_ADD_FAVORITE,
    ERROR_MSG_REMOVE_FAVORITE,
    ERROR_MSG_ADD_CART,
    ERROR_MSG_REMOVE_CART
)
from recipes.models import (
    Ingredient,
    Tag,
    Recipe,
    Favourites,
    ShoppingCart,
    IngredientInRecipe
)
from .pagination import CustomPagination
from .permissions import (
    IsAuthorOrAdminOrReadOnly
)
from .serializers import (
    IngredientsSerializer,
    TagsSerializer,
    RecipeReadSerializer,
    RecipeWriteSerializer,
    RecipeCutSerializer
)


class IngredientsViewSet(ReadOnlyModelViewSet):
    '''Класс представления для ингредиентов.'''

    serializer_class = IngredientsSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        name = self.request.query_params.get('name')
        if name is not None:
            queryset = queryset.filter(name__istartswith=name)
        return queryset


class TagsViewSet(ReadOnlyModelViewSet):
    '''Клас представления для тегов.'''

    queryset = Tag.objects.all()
    serializer_class = TagsSerializer


class RecipeViewSet(ModelViewSet):
    '''Класс представления для рецептов.'''

    queryset = Recipe.objects.prefetch_related('author', 'tags')
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilterSet
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def _add_to(self, user, model, recipe, error_msg):
        '''Вспомогательная функция для добавления рецепта
        в избранное/список покупок.'''

        if model.objects.filter(user=user, recipe=recipe).exists():
            return Response(
                {'errors': error_msg},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = RecipeCutSerializer(recipe)
        model.objects.create(
            user=user,
            recipe=recipe
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _remove_from(self, user, model, recipe, error_msg):
        '''Вспомогательная функция для удаления рецепта
        из избранного/списка покупок.'''

        obj = model.objects.filter(user=user, recipe=recipe)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {'errors': error_msg},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk):
        '''Action добавления рецепта в избранное.'''

        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            return self._add_to(
                user,
                Favourites,
                recipe,
                ERROR_MSG_ADD_FAVORITE
            )
        return self._remove_from(
            user,
            Favourites,
            recipe,
            ERROR_MSG_REMOVE_FAVORITE
        )

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        '''Action добавления рецепта в список покупок.'''

        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            return self._add_to(
                user,
                ShoppingCart,
                recipe,
                ERROR_MSG_ADD_CART
            )
        return self._remove_from(
            user,
            ShoppingCart,
            recipe,
            ERROR_MSG_REMOVE_CART
        )

    @action(
        methods=['get'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        '''Action для скачивания ингредиентов из списка покупок.'''

        shopping_cart = request.user.buyer.all()
        recipes = [obj.recipe_id for obj in shopping_cart]
        ingredients_list = (
            IngredientInRecipe.objects
            .filter(recipe__in=recipes)
            .values('ingredient')
            .annotate(amount=Sum('amount'))
        )
        id_amount_dict = {}
        result = f'Список покупок пользователя {request.user.username}\n'
        for item in ingredients_list:
            id_amount_dict[item['ingredient']] = item['amount']
        ingredients_id_list = list(id_amount_dict.keys())
        ingredients = Ingredient.objects.filter(id__in=ingredients_id_list)
        for key, value in id_amount_dict.items():
            ingredient = ingredients.get(id=key)
            result += (
                f'- {ingredient.name}: {value} {ingredient.measurement_unit}\n'
            )
        response = HttpResponse(result, content_type="text/plain")
        response['Content-Disposition'] = (
            'attachment; filename=shopping-cart.txt'
        )
        return response

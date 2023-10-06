from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers, validators
from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField

from recipes.models import (
    Recipe,
    Ingredient,
    IngredientInRecipe,
    Tag,
    Favourites,
    ShoppingCart,
)
from .errors_msg import (
    ERROR_MSG_EMPTY_INGR,
    ERROR_MSG_EMPTY_TAG,
    ERROR_MSG_NON_EXISTING_INGR,
    ERROR_MSG_DUB_INGR,
    ERROR_MSG_ZERO_AMOUNT_INGR,
    ERROR_MSG_DUB_TAG,
    ERROR_MSG_NON_IMAGE,
    ERROR_MSG_EMPTY
)

User = get_user_model()


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        # lookup_field = 'slug'


class IngredientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        # lookup_field = 'name'


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeIngredientsWriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(write_only=True)
    amount = serializers.IntegerField(write_only=True)

    def validate(self, attrs):
        return super().validate(attrs)

    class Meta:
        model = Ingredient
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    tags = TagsSerializer(many=True, read_only=True)

    def validate_image(self, value):
        if not value:
            raise serializers.ValidationError(ERROR_MSG_NON_IMAGE)
        return value
    
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class RecipeReadSerializer(RecipeSerializer):
    author = UserSerializer()
    ingredients = serializers.SerializerMethodField(
        method_name='get_ingredients'
    )
    is_favorited = serializers.SerializerMethodField(
        method_name='get_is_favorited'
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name='get_is_in_shopping_cart'
    )

    def get_ingredients(self, obj):
        ingredients = IngredientInRecipe.objects.filter(recipe=obj)
        serializer = IngredientInRecipeSerializer(ingredients, many=True)
        return serializer.data

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Favourites.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(user=user, recipe=obj).exists()

    class Meta(RecipeSerializer.Meta):
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart', 'name',
                  'image', 'text', 'cooking_time')
        ordering = ('pk', )


class RecipeWriteSerializer(RecipeSerializer):
    ingredients = RecipeIngredientsWriteSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )

    def validate_ingredients(self, value):
        if not value:
            raise serializers.ValidationError(ERROR_MSG_EMPTY_INGR)
        ingredients = set([item['id'] for item in value])
        if len(ingredients) < len(value):
            raise serializers.ValidationError(ERROR_MSG_DUB_INGR)
        for item in value:
            ingredient = Ingredient.objects.filter(id=item['id'])
            if not ingredient.exists():
                raise serializers.ValidationError(ERROR_MSG_NON_EXISTING_INGR)
            if int(item['amount']) < 1:
                raise serializers.ValidationError(ERROR_MSG_ZERO_AMOUNT_INGR)
        return value
    
    def validate_tags(self, value):
        if not value:
            raise serializers.ValidationError(ERROR_MSG_EMPTY_TAG)
        tags = set(value)
        if len(tags) < len(value):
            raise serializers.ValidationError(ERROR_MSG_DUB_TAG)
        return value

    def _add_ingredients_in_recipe(self, ingredients, recipe):
        for item in ingredients:
            amount = item['amount']
            ingredient = get_object_or_404(Ingredient, id=item['id'])
            IngredientInRecipe.objects.create(
                ingredient=ingredient,
                recipe=recipe,
                amount=amount
            )

    def create(self, validated_data):
        author = self.context.get('request').user
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.tags.set(tags)
        self._add_ingredients_in_recipe(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        try:
            ingredients = validated_data.pop('ingredients')
            tags = validated_data.pop('tags')
        except KeyError as error:
            raise serializers.ValidationError(ERROR_MSG_EMPTY.format(error))
        instance = super().update(instance, validated_data)
        instance.tags.set(tags)
        instance.ingredients.clear()
        self._add_ingredients_in_recipe(ingredients, instance)
        instance.save()
        return instance

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeReadSerializer(instance, context=context).data

    class Meta(RecipeSerializer.Meta):
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        )


class RecipeCutSerializer(RecipeReadSerializer):
    class Meta(RecipeReadSerializer.Meta):
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
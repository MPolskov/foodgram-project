from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from django.shortcuts import get_object_or_404
from djoser.serializers import UserSerializer
# from rest_framework.validators import UniqueTogetherValidator

from recipes.models import (
    Recipe,
    Ingredient,
    IngredientInRecipe,
    Tag,
    Favourites,
    ShoppingCart,

)

from django.contrib.auth import get_user_model
User = get_user_model()


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        lookup_field = 'slug'


class IngredientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurment_unit')
        lookup_field = 'name'


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurment_unit = serializers.ReadOnlyField(
        source='ingredient.measurment_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurment_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    tags = TagsSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe


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


class RecipeIngredientsWriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField(write_only=True)

    class Meta:
        model = Ingredient
        fields = ('id', 'amount')


class RecipeWriteSerializer(RecipeSerializer):
    ingredients = RecipeIngredientsWriteSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )

    class Meta(RecipeSerializer.Meta):
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        )

    def _create_ingredients_in_recipe(self, ingredients, recipe):
        for i in ingredients:
            amount = i['amount']
            ingredient = get_object_or_404(Ingredient, id=i['id'])
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
        self._create_ingredients_in_recipe(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance = super().update(instance, validated_data)
        instance.tags.set(tags)
        instance.ingredients.clear()
        self._create_ingredients_in_recipe(ingredients, instance)
        instance.save()
        return instance

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeReadSerializer(instance, context=context).data


class RecipeAddToSerializer(RecipeReadSerializer):

    class Meta(RecipeSerializer.Meta):
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )

from rest_framework import serializers, status
from djoser.serializers import UserSerializer
from rest_framework.exceptions import ValidationError

from .models import Follow
from .errors_msg import (
    ERROR_MSG_FOLLOW_YOURSELF,
    ERROR_MSG_DUB_FOLLOW
)
from api.serializers import RecipeCutSerializer


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed'
    )

    class Meta(UserSerializer.Meta):
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, following=obj).exists()


class FollowSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField(
        method_name='get_recipes'
    )
    recipes_count = serializers.SerializerMethodField(
        method_name='get_recipes_count'
    )

    def get_recipes(self, obj):
        recipes = obj.recipe.all()
        if 'recipes_limit' in self.context.get('request').GET:
            recipes_limit = self.context.get('request').GET['recipes_limit']
            recipes = recipes[:int(recipes_limit)]
        serializer = RecipeCutSerializer(recipes, many=True, read_only=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.recipe.count()

    def validate(self, data):
        user = self.context.get('request').user
        author = self.instance
        if user == author:
            raise ValidationError(
                ERROR_MSG_FOLLOW_YOURSELF,
                code=status.HTTP_400_BAD_REQUEST
            )
        if user.follower.filter(following=author).exists():
            raise ValidationError(
                ERROR_MSG_DUB_FOLLOW,
                code=status.HTTP_400_BAD_REQUEST
            )

        return data

    class Meta(CustomUserSerializer.Meta):
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )
        read_only_fields = (
            'email',
            'username',
            'first_name',
            'last_name'
        )

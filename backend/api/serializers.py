import base64
from io import BytesIO
from PIL import Image

from rest_framework import serializers

from recipes.models import (
    Recipe,

)

IMAGE_BASE64_ERROR = 'Картинка должна быть кодирована в base64'

class CustomImageField(serializers.Field):  # TODO: Написать кастомное поле для картинок
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            decode = BytesIO(base64.b64decode(data))
            image = Image.open(decode)
        except ValueError:
            raise serializers.ValidationError(IMAGE_BASE64_ERROR)
        return image


class RecipeSerializer(serializers.ModelSerializer):
    image = CustomImageField()
    tags = TagsSerializer(required=False, many=True)
    ingredients = IngredientsSerializer(required=False, many=True)
        
    )

    class Meta:
        model = Recipe
        fields = ('id', 'tags' 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_card', 'name',
                  'text', 'cooking_time')
        ordering = ('pk', )
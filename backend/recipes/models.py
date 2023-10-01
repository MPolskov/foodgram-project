from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import (
    MinValueValidator,
    validate_slug,
)

User = get_user_model()

MIN_VALUE_ERROR = 'Значение не может быть меньше нуля'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор публикации',
        on_delete=models.CASCADE,
        related_name='recipe',
        null=False
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=256
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='media/recipes/'
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='IngredientInRecipe',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        'Tag',
        # through='TagRecipe',
        verbose_name='Теги'
    )
    cooking_time = models.IntegerField(
        validators=(
            MinValueValidator(0, message=MIN_VALUE_ERROR),
        ),
        verbose_name='Время приготовления'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256,
        unique=True
    )
    color = models.CharField(
        verbose_name='Цветовой код',
        max_length=16,
        unique=True
    )
    slug = models.SlugField(
        unique=True,
        validators=(validate_slug,)
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256,
        # unique=True
    )
    measurment_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=16
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE  # TODO: выбрать правильный метод при удалении
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE   # TODO: выбрать правильный метод при удалении
    )
    amount = models.IntegerField(
        validators=(
            MinValueValidator(0, message=MIN_VALUE_ERROR),
        ),
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Рецепты и ингредиенты'
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_ingredient_recipe'
            )
        ]

    def __str__(self):
        return f'{self.recipe} {self.ingredient} {self.amount}'


# class TagRecipe(models.Model):
#     tag = models.ForeignKey(
#         Tag,
#         on_delete=models.CASCADE
#     )
#     recipe = models.ForeignKey(
#         Recipe,
#         on_delete=models.CASCADE
#     )

#     class Meta:
#         verbose_name = 'Рецепты и теги'
#         verbose_name_plural = verbose_name
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['tag', 'recipe'],
#                 name='unique_tag_recipe'
#             )
#         ]

#     def __str__(self):
#         return f'{self.tag} {self.recipe}'


class Favourites(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_favorite'
            )
        ]


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='buyer',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='products',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe'
            )
        ]

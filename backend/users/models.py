from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    '''Модель пользователя.'''

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    DEFAULT_MAX_LENGTH = 150
    EMAIL_MAX_LENGTH = 254

    ADMIN = 'admin'
    USER = 'user'

    ROLES = (
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор')
    )

    username = models.CharField(
        'Логин',
        max_length=DEFAULT_MAX_LENGTH,
        unique=True,
        validators=([RegexValidator(regex=r'^[\w.@+-]+\Z')])
    )
    password = models.CharField(
        'Пароль',
        max_length=DEFAULT_MAX_LENGTH,
        validators=([RegexValidator(regex=r'^[\w.@+-]+\Z')])
    )
    email = models.EmailField(
        'E-mail',
        max_length=EMAIL_MAX_LENGTH,
        unique=True
    )
    first_name = models.CharField(
        'Имя',
        max_length=DEFAULT_MAX_LENGTH,
        validators=([RegexValidator(regex=r'^[\w.@+-]+\Z')])
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=DEFAULT_MAX_LENGTH,
        validators=([RegexValidator(regex=r'^[\w.@+-]+\Z')])
    )
    role = models.CharField(
        'Роль',
        max_length=10,
        choices=ROLES,
        default='user',
    )

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]

    def __str__(self):
        return self.username


class Follow(models.Model):
    '''Модель подписки на автора.'''

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
    )

    class Meta:
        verbose_name = 'Подписки'
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_user_following'
            )
        ]

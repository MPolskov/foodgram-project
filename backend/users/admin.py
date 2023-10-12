from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy

from .models import Follow

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'id',
        'email',
        'first_name',
        'last_name',
        'followers',
        'recipes'
    )
    list_filter = ('email', 'username')
    readonly_fields = ('followers', 'recipes')

    @admin.display(description='Подписчики')
    def followers(self, obj):
        return obj.following.count()

    @admin.display(description='Рецепты')
    def recipes(self, obj):
        return obj.recipe.count()


admin.site.register(Follow)
admin.site.unregister(TokenProxy)
admin.site.unregister(Group)

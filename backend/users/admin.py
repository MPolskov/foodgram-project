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
    )
    list_filter = ('email', 'username')


admin.site.register(Follow)
admin.site.unregister(TokenProxy)
admin.site.unregister(Group)

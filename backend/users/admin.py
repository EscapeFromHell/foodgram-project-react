from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from foodgram.settings import EMPTY_VALUE_DISPLAY

from .models import Subscribe, User


@admin.register(User)
class UserAdmin(UserAdmin):
    model = User
    list_display = (
        'id', 'email', 'username', 'first_name', 'last_name', 'is_blocked',
        'is_superuser',
    )
    list_filter = (
        'email', 'username', 'is_blocked', 'is_superuser',
    )
    search_fields = ('email', 'username', 'first_name', 'last_name',)
    ordering = ('id', 'email', 'username',)


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('user', 'author',)
    empty_value_display = EMPTY_VALUE_DISPLAY

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

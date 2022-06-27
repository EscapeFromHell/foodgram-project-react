from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models


class User(AbstractUser, PermissionsMixin):
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True
    )

    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=False,
        null=False
    )

    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=False,
        null=False
    )

    password = models.CharField(
        'Пароль',
        max_length=150,
    )

    email = models.EmailField(
        'Почта',
        max_length=254,
        unique=True
    )

    is_superuser = models.BooleanField(
        'Администратор',
        default=False
    )

    is_blocked = models.BooleanField(
        'Заблокирован',
        default=False
    )

    class Meta:
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['email', 'username'],
                name='unique_auth'
            ),
        ]
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_superuser


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribing',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author',),
                name='unique_subscribe',
            ),
        )

    def __str__(self):
        return f'{self.user} -> {self.author}'

import api_yamdb.settings as settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from .validators import validate_username


class User(AbstractUser):
    username = models.CharField(
        'Имя пользователя', max_length=150, unique=True,
        null=False, blank=False, validators=(validate_username,))
    email = models.EmailField(
        'Электронная почта', max_length=254, unique=True,
        null=False, blank=False)
    first_name = models.CharField('Имя', max_length=150, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Пользовательская роль',
        max_length=20,
        choices=settings.ROLE_CHOICES,
        default=settings.USER,
    )
    confirmation_code = models.TextField('Код подтверждения')

    def is_admin(self):
        return (self.role == settings.ADMIN or self.is_superuser
                or self.is_staff)

    def is_moderator(self):
        return self.role == settings.MODERATOR

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['username']

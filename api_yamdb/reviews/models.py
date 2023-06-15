from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.constraints import UniqueConstraint


class User(AbstractUser):
    username = models.CharField(
        'Имя пользователя', max_length=150, unique=True)
    email = models.EmailField(
        'Электронная почта', max_length=254, unique=True)
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)
    bio = models.TextField('Биография')
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
        constraints = [UniqueConstraint(
            fields=['username', 'email'],
            name='unique_registry')]
        ordering = ['username']


class Category(models.Model):
    name = models.CharField(
        'Название категории', max_length=256, unique=True)
    slug = models.SlugField('Слаг', max_length=50)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        'Жанр произведения', max_length=256, unique=True)
    slug = models.SlugField('Слаг', max_length=50)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        'Название произведения',max_length=256)
    year = models.PositiveIntegerField('Год выпуска произведения')
    description = models.TextField('Описание произведения')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles', null=True)
    genre = models.ManyToManyField(Genre, related_name='titles')

    def __str__(self):
        return self.name

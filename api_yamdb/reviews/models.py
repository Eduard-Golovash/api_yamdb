from django.contrib.auth.models import AbstractUser
from django.db import models


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
        choices=[
            ('user', 'User'),
            ('moderator', 'Moderator'),
            ('admin', 'Admin'),
        ],
        default='user'
    )


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

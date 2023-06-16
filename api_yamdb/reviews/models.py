from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models.constraints import UniqueConstraint
from django.core.validators import MinValueValidator, MaxValueValidator
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


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        verbose_name='Произведение',
        related_name='rewiews'
    )
    text = models.TextField(
        verbose_name='Отзыв',
        help_text='Текст отзыва'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='reviews'
    )
    score = models.IntegerField(
        null=True,
        default=None,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review',
            ),
        )

    def __str__(self) -> str:
        return self.text[:15]


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор',
                               related_name='comments')
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               verbose_name='Отзыв',
                               related_name='comments')
    text = models.TextField(verbose_name='Комментарий',
                            help_text='Текст комментария')
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True)

    def __str__(self) -> str:
        return self.text
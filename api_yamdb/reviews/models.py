from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from reviews.validators import validate_year
from users.models import User


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = 'Категория'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256
    )
    year = models.IntegerField(
        verbose_name='Дата выхода',
        validators=[validate_year]
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )

    class Meta:
        verbose_name = 'Произведение'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        verbose_name='Произведение',
        related_name='reviews'
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
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10, message='Оценка должна быть от 1 до 10')
        ]
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
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

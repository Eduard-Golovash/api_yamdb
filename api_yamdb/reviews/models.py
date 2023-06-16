from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


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

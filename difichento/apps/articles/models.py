from django.db import models
from django.utils import timezone
import datetime


class Article(models.Model):
    article_title = models.CharField('Название статьи', max_length=100)
    article_text = models.TextField('Текст статьи', max_length=10 ** 5)
    pub_date = models.DateTimeField('Дата публикации')

    def __str__(self):
        return self.article_title

    def was_published_recently(self):
        return self.pub_date >= (timezone.now() - datetime.timedelta(days=3))

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)  # Модель, к которой привязана данная
    author_name = models.CharField('Имя автора', max_length=100)
    comment_text = models.CharField('Текст комментария', max_length=5 * 10 ** 3)

    def __str__(self):
        return self.author_name

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

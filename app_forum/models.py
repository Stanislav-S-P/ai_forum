from django.contrib.auth.models import User
from django.db import models


class News(models.Model):
    """
    Класс - модель таблицы Новостей
    """
    author = models.ForeignKey(User, null=True, blank=True, related_name='news',
                               on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField(max_length=500, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Содержание')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')

    def __str__(self):
        return f'{self.author} - {self.title}'

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        db_table = 'news'
        ordering = ['-created_at']


class Images(models.Model):
    """
    Класс - модель таблицы Изображений
    """
    news = models.ForeignKey(News, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
        db_table = 'images'


class Comments(models.Model):
    """
    Класс - модель таблицы Комментарии
    """
    user = models.ForeignKey(User, null=True, blank=True, related_name='comments', on_delete=models.CASCADE)
    user_name = models.CharField(max_length=30, blank=True, verbose_name='Имя пользователя')
    text_comment = models.CharField(max_length=100, verbose_name='Комментарий')
    new = models.ForeignKey('News',  on_delete=models.CASCADE, related_name='comments', verbose_name='новость')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        db_table = 'comments'

from django.conf import settings
from django.db import models


class Post(models.Model):

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='posts',
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    image = models.ImageField(upload_to='posts/', verbose_name='Изображение')
    caption = models.TextField(blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author}: {self.caption[:30]}'
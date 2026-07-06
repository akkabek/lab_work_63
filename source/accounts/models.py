from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    class Gender(models.TextChoices):
        MALE = 'male', 'Мужской'
        FEMALE = 'female', 'Женский'

    email = models.EmailField('email address', unique=True)
    avatar = models.ImageField(upload_to='avatars/',blank=True,null=True,verbose_name='Аватар')
    bio = models.TextField(blank=True,verbose_name='Информация о пользователе',)
    phone_number = models.CharField(max_length=20,blank=True,verbose_name='Номер телефона',)
    gender = models.CharField(max_length=10,choices=Gender.choices,blank=True,verbose_name='Пол')

    def __str__(self):
        return self.username

    @property
    def posts_count(self):
        return self.posts.count() if hasattr(self, 'posts') else 0

    @property
    def followers_count(self):
        return self.followers.count() if hasattr(self, 'followers') else 0

    @property
    def following_count(self):
        return self.following.count() if hasattr(self, 'following') else 0

class Follow(models.Model):

    follower = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
    )
    following = models.ForeignKey(
        User,
        related_name='followers',
        on_delete=models.CASCADE,
        verbose_name='Автор, на которого подписались',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['follower', 'following'], name='unique_follow'
            ),
            models.CheckConstraint(
                check=~models.Q(follower=models.F('following')),
                name='cannot_follow_self',
            ),
        ]

    def __str__(self):
        return f'{self.follower} -> {self.following}'
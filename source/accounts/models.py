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
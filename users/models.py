from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта ')

    phone = models.CharField(max_length=35, verbose_name='Номер телефон',
                             **NULLABLE)
    country = models.CharField(max_length=35, verbose_name='Страна',
                               **NULLABLE)
    avatar = models.ImageField(upload_to='users_images/', verbose_name='Аватар',
                               **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

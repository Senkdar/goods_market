from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class CustomUser(AbstractUser):
    """Модель пользователя"""
    last_name = models.CharField('Фамилия', max_length=256)
    first_name = models.CharField('Имя', max_length=256)
    patronymic = models.CharField(
        'Отчество',
        max_length=256,
        blank=True,
        null=True
    )
    email = models.EmailField(unique=True)
    password = models.CharField('Пароль', max_length=150)
    phone_validator = RegexValidator(
            regex=r'^8-\d{3}-\d{3}-\d{2}-\d{2}$',
            message="Номер телефона должен быть в формате: '8-xxx-xxx-xx-xx'"
        )
    phone_number = models.CharField(
        'Номер телефона',
        max_length=17,
        unique=True,
        validators=[phone_validator,]
    )

    def __str__(self):
        return (f'{self.first_name} {self.last_name}')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

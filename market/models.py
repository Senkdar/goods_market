from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class CustomUser(AbstractUser):
    """Модель пользователя."""
    username = models.CharField(max_length=256, unique=True)
    last_name = models.CharField('Фамилия', max_length=256)
    first_name = models.CharField('Имя', max_length=256)
    patronymic = models.CharField(
        'Отчество',
        max_length=256,
        blank=True,
        null=True
    )
    email = models.EmailField('Имя пользователя', unique=True)
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
        return (self.username)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Goods(models.Model):
    """Модель товаров для заказа."""
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='goods'
    )
    name = models.CharField('Название', max_length=150)
    link = models.URLField('Ссылка')
    comment = models.CharField('комментарий', max_length=300)

    def __str__(self):
        return (self.name)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Order(models.Model):
    """Модель заказа."""
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Пользователь',
    )
    goods = models.ManyToManyField(
        Goods,
        verbose_name='Товары',
    )
    pub_date = models.DateTimeField(
        'дата публикации',
        auto_now_add=True,
    )
    status = models.CharField(max_length=150, default='created')
    processed_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name='processed_orders',
        verbose_name='обработал заказ',
        blank=True,
        null=True,
    )
    processed_at = models.DateTimeField(
        'дата обработки заказа',
        auto_now_add=True,
        blank=True,
        null=True,
    )
    comment = models.TextField(
        'Причина',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

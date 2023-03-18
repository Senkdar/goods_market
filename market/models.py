from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models


class CustomUserManager(BaseUserManager):
    """Менеджер для модели пользователя."""
    def create_user(self, email, password, **extra_fields):
        """Создание пользователя"""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Создание суперпользователя"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


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
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=150)
    phone_validator = RegexValidator(
            regex=r'^8-\d{3}-\d{3}-\d{2}-\d{2}$',
            message="Номер телефона должен быть в формате: '8-xxx-xxx-xx-xx'"
        )
    phone_number = models.CharField(
        'Номер телефона',
        max_length=17,
        # unique=True,
        validators=[phone_validator,]
    )


    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['last_name', 'first_name',]

    # objects = CustomUserManager()

    def __str__(self):
        return (f'{self.first_name} {self.last_name}')

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

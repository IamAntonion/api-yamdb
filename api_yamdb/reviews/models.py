from django.core.validators import (MaxValueValidator,
                                    MinValueValidator)
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.timezone import now

from . import constants


def not_me_validator(value):
    if value == 'me':
        raise ValidationError('Имя "me" запрещено.')


class User(AbstractUser):

    class Role(models.TextChoices):
        USER = 'user', 'Пользователь'
        MODERATOR = 'moderator', 'Модератор'
        ADMIN = 'admin', 'Администратор'

    username = models.CharField(
        max_length=constants.USERNAME_MAX_LENTGH,
        unique=True,
        validators=[UnicodeUsernameValidator(), not_me_validator]
    )
    email = models.EmailField(unique=True)
    confirmation_code = models.SlugField(default='0',)
    # is_moderator = models.BooleanField(default=False)
    bio = models.TextField(
        max_length=constants.BIO_MAX_LENGTH,
        blank=True,
        verbose_name='О себе'
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER,
        verbose_name='Роль'
    )

    class Meta:
        ordering = ['id']

    @property
    def is_admin(self):
        return (self.role == self.Role.ADMIN
                or self.is_superuser
                or self.is_staff)

    @property
    def is_moderator(self):
        return self.role == self.Role.MODERATOR

    def __str__(self):
        return self.username


class SlugModel(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
        unique=True
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='Слаг',
        unique=True
    )

    class Meta:
        abstract = True
        ordering = ('name',)
        verbose_name = 'Общая модель'
        verbose_name_plural = 'Общие модели'

    def __str__(self):
        return self.name


class Category(SlugModel):
    class Meta(SlugModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(SlugModel):
    class Meta(SlugModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название'
    )
    year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(-32768),
            MaxValueValidator(now().year)
        ],
        db_index=True,
        verbose_name='Год выпуска'
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанры'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория')

    class Meta:
        ordering = ('name', '-year')
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        default_related_name = 'titles'

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(1, 'Оценка не может быть меньше 1'),
            MaxValueValidator(10, 'Оценка не может быть больше 10')
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_review'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text

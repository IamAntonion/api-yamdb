from django.db import models


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

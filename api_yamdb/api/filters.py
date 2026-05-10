import django_filters
from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    """Фильтр для TitleViewSet."""

    # Фильтр по имени
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )
    # Фильтр по году выпуска
    year = django_filters.NumberFilter(
        field_name='year',
    )
    # Фильтр по жанру
    genre = django_filters.CharFilter(
        field_name='genre__slug',
        lookup_expr='icontains'
    )
    # Фильтр по категории
    category = django_filters.CharFilter(
        field_name='category__slug',
        lookup_expr='icontains'
    )

    class Meta:
        model = Title
        fields = [
            'name',
            'year',
            'genre',
            'category'
        ]

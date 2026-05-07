from rest_framework import viewsets, mixins, filters
from rest_framework.pagination import PageNumberPagination

from django.db.models import Avg

from reviews.models import (
    Category,
    Genre,
    Title)
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleCreateSerializer,
    TitleSerializer
)
from .permissions import IsAdminUserOrReadOnly
from .filters import TitleFilter


class BaseSlugViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminUserOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    http_method_names = ['get', 'post', 'delete', 'head', 'options']


class CategoryViewSet(BaseSlugViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(BaseSlugViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by(*Title.Meta.ordering)
    serializer_class = TitleSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = [
        filters.OrderingFilter,
        filters.DjangoFilterBackend
    ]
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitleCreateSerializer
        return TitleSerializer

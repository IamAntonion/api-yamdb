

from .permissions import IsAuthorModeratorAdminOrReadOnly

# ЗАМЕТКА ДЛЯ РАЗРАБОТЧИКА №2 (Titles):
# В твоем TitleSerializer обязательно добавь поле 'rating'.
# ТЗ требует среднюю оценку. Сделай это через:
# queryset = Title.objects.annotate(rating=Avg('reviews__score'))
# .order_by('name')

from rest_framework import (
    generics,
    viewsets,
    filters,
    mixins,
    status
)
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from .filters import TitleFilter

from .permissions import IsAdmin, IsAuthenticatedUser, IsModerator
from .pagination import UserPagination
from .serializers import (
    SignUpSerializer,
    TokenSerializer,
    UserSerializer,
    UserMeSerializer,
    CategorySerializer,
    GenreSerializer,
    TitleCreateSerializer,
    TitleSerializer,
    ReviewSerializer,
    CommentSerializer
)

from reviews.models import (
    Category,
    Genre,
    Review, 
    Title
)


User = get_user_model()

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)

    def get_review(self):
        return get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class SignUpView(generics.CreateAPIView):

    serializer_class = SignUpSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "email": user.email,
                "username": user.username
            },
            status=status.HTTP_200_OK
        )


class TokenView(generics.GenericAPIView):

    serializer_class = TokenSerializer
    permission_classes = []

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data

        refresh = RefreshToken.for_user(user)

        response_data = {
            'token': str(refresh.access_token),
        }
        return Response(response_data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    pagination_class = UserPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ('role',)
    permission_classes = [
        IsAdmin,]


class CurrentUserView(generics.RetrieveUpdateAPIView):

    serializer_class = UserMeSerializer
    permission_classes = [IsAuthenticatedUser,]

    def get_object(self):
        return self.request.user

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

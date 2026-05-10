from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    # CurrentUserView,
    SignUpView,
    TokenView,
    UserViewSet,
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewViewSet,
    CommentViewSet
)

router_v1 = DefaultRouter()
router_v1.register(
    r'users',
    UserViewSet,
    basename='users'
)
router_v1.register(
    r'categories',
    CategoryViewSet,
    basename='categories'
)
router_v1.register(
    r'genres',
    GenreViewSet,
    basename='genres'
)
router_v1.register(
    r'titles',
    TitleViewSet,
    basename='titles'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

VERSION_PREFIX = 'v1'

auth_patterns = [
    path('signup/', SignUpView.as_view(), name='sign_up'),
    path('token/', TokenView.as_view(), name='get_token'),
]

urlpatterns = [
    # path(f'{VERSION_PREFIX}/users/me/', CurrentUserView.as_view(), name='users_me'),
    path(f'{VERSION_PREFIX}/', include(router_v1.urls)),
    path(f'{VERSION_PREFIX}/auth/', include(auth_patterns)),
]

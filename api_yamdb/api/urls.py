from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
  SignUpView,
  TokenView,
  UserViewSet,
  CurrentUserView,
  CategoryViewSet,
  GenreViewSet,
  TitleViewSet
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

VERSION_PREFIX = 'v1'

urlpatterns = [
    path(f'{VERSION_PREFIX}/auth/signup/',
         SignUpView.as_view(),
         name='sign_up'),
    path(f'{VERSION_PREFIX}/auth/token/',
         TokenView.as_view(),
         name='get_token'),
    path(f'{VERSION_PREFIX}/users/me/',
         CurrentUserView.as_view(),
         name='current_user'),
    path(f'{VERSION_PREFIX}',
         include(router_v1.urls)),
]

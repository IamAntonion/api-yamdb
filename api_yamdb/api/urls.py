from django.urls import path, include
from .views import SignUpView, TokenView, UserViewSet, CurrentUserView
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('users', UserViewSet, basename='users')

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
    path(f'{VERSION_PREFIX}/',
         include(router.urls)),
]

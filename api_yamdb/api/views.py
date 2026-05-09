from rest_framework import status
from rest_framework import generics, viewsets, filters
from .serializers import (SignUpSerializer,
                          TokenSerializer,
                          UserSerializer,
                          UserMeSerializer)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .permissions import IsAdmin, IsAuthenticatedUser, IsModerator
from .pagination import UserPagination


User = get_user_model()


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

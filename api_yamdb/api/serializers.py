from rest_framework import serializers

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings

from reviews.models import (
    Category,
    Genre,
    Title,
    Review,
    Comment
)

import re


User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений."""

    genre = GenreSerializer(
        many=True,
        read_only=True
    )
    category = CategorySerializer(
        read_only=True
    )
    rating = serializers.IntegerField(
        read_only=True
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
        read_only_fields = fields


class TitleCreateSerializer(serializers.ModelSerializer):
    """Сериализатор произведений для создания и редактирования."""

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        allow_empty=False
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )

    def to_representation(self, instance):
        return TitleSerializer(instance).data


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    def validate(self, data):
        """
        Проверяет уникальность отзыва пользователя на произведение.

        Пользователь может оставить только один отзыв на одно произведение.
        """
        request = self.context.get('request')

        if request.method != 'POST':
            return data

        author = request.user

        title = self.context.get('view').get_title()

        if title.reviews.filter(author=author).exists():
            raise serializers.ValidationError(
                'Вы уже оставили отзыв на это произведение.'
            )

        return data

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class SignUpSerializer(serializers.Serializer):
    """Сериализатор регистрации пользователя."""

    username = serializers.CharField(
        max_length=150,
        required=True,
    )
    email = serializers.EmailField(
        max_length=150,
        required=True,
    )

    def validate(self, attrs):
        """
        Проверяет корректность username и email.

        Проверка:
        - запрещенные символы;
        - имя "me";
        - уникальность.
        """
        username = attrs.get('username')
        email = attrs.get('email')
        errors = {}

        invalid_chars = re.findall(r'[^\w.@+-]', username)
        if invalid_chars:
            forbidden_chars = ''.join(set(invalid_chars))
            raise ValidationError(
                f'Недопустимый username. Запрещенные символы: {forbidden_chars}'
            )

        if username == 'me' or '$' in username:
            raise serializers.ValidationError(
                {'username': f'Недопустимое имя пользователя - {username}'})

        if User.objects.filter(
                username=username).exclude(email=email).exists():
            errors[
                'username'] = 'Это имя пользователя уже занято другим email.'

        if User.objects.filter(
                email=email).exclude(username=username).exists():
            errors[
                'email'] = 'Этот email уже используется другим пользователем.'

        if not errors:
            return attrs

        raise serializers.ValidationError(errors)

    def create(self, validated_data):
        """
        Создает пользователя и отправляет confirmation_code.

        Если пользователь существует отправляет confirmation code.
        """
        username = validated_data['username']
        email = validated_data['email']
        try:
            user = User.objects.get(
                username=username,
                email=email)
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=username,
                email=email,
                is_active=True
            )
        user.confirmation_code = get_random_string(length=40)
        user.save()

        send_mail(
            subject='Ваш верификационный код',
            message=f'Ваш код: {user.confirmation_code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=(validated_data['email'],),
            fail_silently=False,
        )

        return user


class TokenSerializer(serializers.Serializer):
    """Сериализатор получения JWT-токена."""

    username = serializers.CharField(
        max_length=150,
        required=True,
    )
    confirmation_code = serializers.SlugField(
        required=True,
    )

    def validate(self, data):
        """
        Проверяет confirmation_code пользователя.

        Если код корректный - очищает его и возвращает пользователя.
        """
        username = data.get('username')
        code = data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if user.confirmation_code != code:
            raise serializers.ValidationError('Неверный confirmation_code')
        user.confirmation_code = ''
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')
        read_only_fields = ('id', 'date_joined')

    def update(self, instance, validated_data):
        cleaned_data = validated_data.copy()
        cleaned_data.pop('role', None)
        return super().update(instance, cleaned_data)

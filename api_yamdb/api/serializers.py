from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .utils import send_confurm_mail
from django.utils.crypto import get_random_string


User = get_user_model()


class SignUpSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        errors = {}
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
        send_confurm_mail(user.confirmation_code,
                          (validated_data['email']))
        return user


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.SlugField()

    def validate(self, data):
        username = data.get('username')
        code = data.get('confirmation_code')
        user = get_object_or_404(
            User,
            username=username,
            confirmation_code=code)
        user.confirmation_code = ''
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')
        read_only_fields = ('id', 'date_joined')


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'email',
                  'first_name',
                  'last_name',
                  'date_joined')
        read_only_fields = ('id', 'username', 'date_joined')
        extra_kwargs = {
            'email': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

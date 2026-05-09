from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    confirmation_code = models.SlugField(default='0',)
    is_moderator = models.BooleanField(default=False)
    bio = models.TextField(max_length=500, blank=True, verbose_name="О себе")
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user', verbose_name="Роль")

    def __str__(self):
        return self.username
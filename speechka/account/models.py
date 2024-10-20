from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.urls import reverse
from datetime import date, timedelta


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True, blank=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email




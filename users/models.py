from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, name=None, **extra_fields):
        if not username:
            raise ValueError("The Username field is required")
        user = self.model(username=username, name=name, **extra_fields)
        user.set_password(password)  # hash password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, name=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, name, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=128)  # handled by AbstractBaseUser
    
    # Only keep is_active + is_superuser (from PermissionsMixin)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.username

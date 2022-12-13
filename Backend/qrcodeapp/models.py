from django.db import models
from datetime import date, datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# from django.contrib.auth.models import User

# from django.contrib.auth.password_validation import validate_password

# from django.conf import settings
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users Should have an Email')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Password should not be empty')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=225, unique=True, db_index=True)
    email = models.EmailField(max_length=225, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # class Meta:
    #     ordering = ['email']
    #     verbose_name = "User"

    # Tell Django how to manage updates of this type of users

    objects = UserManager()

    def __str__(self):
        return str(self.email)

    def tokens(self):
        return ''


# class Users(AbstractUser):
#     first_name = models.CharField(max_length=60)
#     last_name = models.CharField(max_length=60)
#     username = models.CharField(max_length=20, unique=True)
#     email = models.EmailField(max_length=50)
#     password = models.TextField(validators=[validate_password])
#     password2 = models.TextField()
#     isLoggedIn = models.BooleanField(default=False)

#     def __str__(self):
#         return f'{self.first_name} {self.last_name}'

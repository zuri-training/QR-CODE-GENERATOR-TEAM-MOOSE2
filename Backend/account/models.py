from django.db import models

# Create your models here.


from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, Permission, Group
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
import requests



GENDER = (
    ('MALE', "MALE"),
    ('UNSPECIFIED', "UNSPECIFIED"),
    ('FEMALE', "FEMALE"),
)


class CustomUserManager(BaseUserManager):
    # use_in_migrations = True
    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username, email, password, **extra_fields)






class User(AbstractUser):
    username = models.CharField(max_length=60, unique=True)  # username are stored in lower case
    first_name = models.CharField(_('first name'), max_length=1000)
    last_name = models.CharField(_('last name'), max_length=150)
    email = models.CharField(max_length=70)
    phone_number = models.CharField(max_length=70, null=True, blank=True)
    temp_verification_link = models.URLField(null=True, blank=True)
    temp_password = models.CharField(max_length=60, blank=True)
    email_activated = models.BooleanField(default=False)
    email_activated_at = models.DateTimeField(blank=True, null=True)
    gender = models.CharField(
        max_length=20, choices=GENDER, default='UNSPECIFIED', blank=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    is_default = models.BooleanField(default=False)

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ('-pk',)

    def __str__(self):
        return f"{self.username}-{self.full_name()}"

    def full_name(self):
        return self.get_full_name().replace(',', "'")

    def get_user_permissions_list(self):
        try:
            perms = Permission.objects.filter(content_type__app_label=User._meta.app_label,
                                              content_type__model=User._meta.model_name, user=self).order_by('codename')
            return list(set([x.codename for x in perms]))
        except:
            return []

    def natural_key(self):
        return f'{self.first_name} {self.last_name}'





















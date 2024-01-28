#  Created by Xudoyberdi Egamberdiyev
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan


from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, is_staff=False, is_superuser=False, **extra_fields):
        user = self.model(username=username, is_staff=is_staff, is_superuser=is_superuser,
                          **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        return self.create_user(username, password, is_staff=True, is_superuser=True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('Username'), unique=True, max_length=50)
    email = models.CharField(max_length=255, null=True, blank=True)

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    lang = models.CharField(default='uz', max_length=2, choices=[
        ("uz", 'uz'),
        ("ru", 'ru'),
        ("en", 'en')
    ])
    ut = models.SmallIntegerField(verbose_name="User Type", default=2, choices=[
        (1, 'Admin'),
        (2, "User"),
    ])  # user type

    created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True, editable=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['ut']

    def save(self, *args, **kwargs):

        return super(User, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "1. Users"

    # def __init__(self, *args, **kwargs):
    #     super(User, self).__init__(*args, **kwargs)
    #     self.fio = self.full_name()

    def get_uname(self):
        return self.username or getattr(self, self.USERNAME_FIELD) or "not set yet"

    def show_phone(self):
        return f"{self.phone[:3]}" + " ** *** ** " + f"{self.phone[-2:]}"

    def __str__(self):
        return getattr(self, self.USERNAME_FIELD)

    def personal(self):
        ut = {1: 'Admin',
              2: "Teacher",
              3: "Student",
              }[self.ut]
        return {
            'lang': self.lang,
            'user_type': ut,
            "username": self.username,
        }

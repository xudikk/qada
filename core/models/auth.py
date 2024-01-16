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
    def create_user(self, phone, password, is_staff=False, is_superuser=False, **extra_fields):
        user = self.model(phone=phone, is_staff=is_staff, is_superuser=is_superuser,
                          **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, password, **extra_fields):
        return self.create_user(phone, password, is_staff=True, is_superuser=True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(_('Phone'), unique=True, max_length=50)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
    avatar = models.ImageField(max_length=255, null=True, upload_to='avatar')
    gender = models.BooleanField(default=True, choices=[(True, "Erkak 👨‍🎓"), (False, "Ayol 🙍‍♀")])
    username = models.CharField(max_length=50, null=True, blank=True)

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    everf = models.BooleanField(default=False, editable=False)  # email verification
    lang = models.CharField(default='uz', max_length=2, choices=[("uz", 'uz'), ("ru", 'ru'), ("en", 'en')])
    ut = models.SmallIntegerField(verbose_name="User Type", default=3, choices=[
        (1, 'Admin'),
        (2, "Teacher"),
        (3, "Student"),
    ])  # user type

    created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True, editable=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['ut']

    def save(self, *args, **kwargs):
        if self.ut == 3:
            self.specialty = "Fintech Student"
            self.level = "Beginner"

        return super(User, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "1. Users"

    def full_name(self):
        return f"{self.first_name} {self.last_name or ''}"

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.fio = self.full_name()

    def get_uname(self):
        return self.username or getattr(self, self.USERNAME_FIELD) or "not set yet"

    def show_phone(self):
        return f"{self.phone[:3]}" + " ** *** ** " + f"{self.phone[-2:]}"

    def __str__(self):
        return self.full_name()

    def personal(self):
        ut = {1: 'Admin',
              2: "Teacher",
              3: "Student",
              }[self.ut]
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'mobile': self.phone,
            'lang': self.lang,
            'user_type': ut,
            'gender': self.gender,
            'level': self.level,
            "spec": self.specialty,
            "username": self.username,
            "email": self.everf
        }

#  Created by Xudoyberdi Egamberdiyev
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan
from django.db import models

from core.models import User


class Qada(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    bomdod = models.CharField(max_length=56, choices=[
        ("bg-success", "Vaqtida o`qildi"),
        ("bg-warning", "Qazosi o`qildi"),
        ("bg-danger", "Qazo bo`ldi"),
    ], default='bg-danger')
    peshin = models.CharField(max_length=56, choices=[
        ("bg-success", "Vaqtida o`qildi"),
        ("bg-warning", "Qazosi o`qildi"),
        ("bg-danger", "Qazo bo`ldi"),
    ], default='bg-danger')
    asr = models.CharField(max_length=56, choices=[
        ("bg-success", "Vaqtida o`qildi"),
        ("bg-warning", "Qazosi o`qildi"),
        ("bg-danger", "Qazo bo`ldi"),
    ], default='bg-danger')
    shom = models.CharField(max_length=56, choices=[
        ("bg-success", "Vaqtida o`qildi"),
        ("bg-warning", "Qazosi o`qildi"),
        ("bg-danger", "Qazo bo`ldi"),
    ], default='bg-danger')
    xufton = models.CharField(max_length=56, choices=[
        ("bg-success", "Vaqtida o`qildi"),
        ("bg-warning", "Qazosi o`qildi"),
        ("bg-danger", "Qazo bo`ldi"),
    ], default='bg-danger')
    vitr = models.CharField(max_length=56, choices=[
        ("bg-success", "Vaqtida o`qildi"),
        ("bg-warning", "Qazosi o`qildi"),
        ("bg-danger", "Qazo bo`ldi"),
    ], default='bg-danger')




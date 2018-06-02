from django.db import models

from django.contrib.auth.models import User
from django.db import models
from datetime import date
from datetime import datetime
from transliterate import translit, get_available_language_codes

class Attitude(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True)
    code = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Attitude'
        verbose_name_plural = 'Attitude'


class Importance(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True)
    code = models.CharField(max_length=250, blank=True, null=True)
    level = models.IntegerField(default=0)
    is_severe = models.NullBooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Importance'
        verbose_name_plural = 'Importances'


class Room(models.Model):
    title = models.CharField(max_length=250, blank=True, null=True)


class ChatSession(models.Model):
    pass


class Message(models.Model):
    pass


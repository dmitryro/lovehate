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
    creator = models.ForeignKey(User,
                                blank=True,
                                null=True,
                                related_name='creator',
                                on_delete=models.CASCADE)
    name = models.CharField(max_length=250, blank=True, null=True)
    is_active = models.NullBooleanField(default=False, blank=True, null=True)
    last_entered = models.DateTimeField(blank=True, null=True)
    last_left = models.DateTimeField(blank=True, null=True)
    is_empty = models.NullBooleanField(default=False, blank=True, null=True)
    is_idle = models.NullBooleanField(default=False, blank=True, null=True)
    time_terminated = models.DateTimeField(blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'

    def __str__(self):
        return self.name



class ChatSession(models.Model):
    user = models.ForeignKey(User,
                             blank=True,
                             null=True,
                             related_name='chat_user',
                             on_delete=models.CASCADE)

    room =  models.ForeignKey(Room,
                             blank=True,
                             null=True,
                             related_name='chat_room',
                             on_delete=models.CASCADE)

    time_joined = models.DateTimeField(auto_now_add=True)
    time_left = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Chat Session'
        verbose_name_plural = 'Chat Sessions'


class Message(models.Model):
    room = models.ForeignKey(Room,
                             blank=True,
                             null=True,
                             related_name='room',
                             on_delete=models.CASCADE)

    color = models.CharField(max_length=250,
                             blank=True,
                             default='#000000',
                             null=True)

    seenby = models.ManyToManyField(User, related_name='seen_by', blank=True)
    receivers = models.ManyToManyField(User, blank=True, null=True)

    subject = models.CharField(max_length=250,
                               blank=True,
                               null=True)

    body = models.TextField(blank=True,
                            null=True)

    is_sent = models.NullBooleanField(default=False, blank=True, null=True)

    time_sent = models.DateTimeField(auto_now_add=True)

    sender = models.ForeignKey(User,
                               blank=True,
                               null=True,
                               related_name='chat_message_sender',
                               on_delete=models.CASCADE)

    attitude = models.ForeignKey(Attitude,
                                 blank=True,
                                 null=True,
                                 related_name='chat_attitude',
                                 on_delete=models.CASCADE)

    importance = models.IntegerField(default=0)

    ip_address = models.CharField(max_length=40,
                                  blank=True,
                                  null=True)
    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def __str__(self):
        return self.body

    

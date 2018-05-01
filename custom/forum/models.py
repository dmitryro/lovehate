from django.contrib.auth.models import User
from django.db import models
from datetime import date


class Attitude(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True)
    code = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        verbose_name = 'Attitude'
        verbose_name_plural = 'Attitude'



class Emotion(models.Model):
    user = models.ForeignKey(User, blank=True, null=True,  on_delete=models.CASCADE)
    subject = models.CharField(max_length=250, blank=True, null=True)
    emotion = models.TextField(blank=True, null=True)
    time_published = models.DateTimeField(auto_now_add=True)
    rating =  models.FloatField(default=0, blank=True, null=True)
    attitude = models.ForeignKey(Attitude, blank=True, null=True, on_delete=models.CASCADE) 

    class Meta:
        verbose_name = 'Emotion'
        verbose_name_plural = 'Emotions'


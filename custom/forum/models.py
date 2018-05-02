from django.contrib.auth.models import User
from django.db import models
from datetime import date
from datetime import datetime
from transliterate import translit, get_available_language_codes

class Attitude(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True)
    code = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        verbose_name = 'Attitude'
        verbose_name_plural = 'Attitude'

class Emotion(models.Model):
    user = models.ForeignKey(User, 
                             blank=True, 
                             null=True,  
                             on_delete=models.CASCADE)
    subject = models.CharField(max_length=250, 
                               blank=True, 
                               null=True)

    translit_subject = models.CharField(max_length=250,
                                        blank=True,
                                        null=True)

    emotion = models.TextField(blank=True, 
                               null=True)
    time_published = models.DateTimeField(auto_now_add=True)
    rating =  models.FloatField(default=0, 
                                blank=True, 
                                null=True)
    attitude = models.ForeignKey(Attitude, 
                                 blank=True, 
                                 null=True, 
                                 on_delete=models.CASCADE) 

#    @property
 #   def subject_translit(self):
 #       return translit(str(self.subject), reversed=True)

    @property
    def date_published(self):
        dt = str(self.time_published)
        year = dt[0:4]
        month = dt[5:7]
        day = dt[8:10]
        return "{}/{}/{}".format(day,
                                 month,
                                 year)

    class Meta:
        verbose_name = 'Emotion'
        verbose_name_plural = 'Emotions'


class Topic(models.Model):
    name = models.CharField(max_length=250,
                            blank=True,
                            null=True)
    translit_name = models.CharField(max_length=250,
                                     blank=True,
                                     null=True)
    time_published = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    @property
    def lovers(self):
       lovers = Emotion.objects.filter(subject=self.name, attitude_id=1)
       return lovers

    @property
    def mehs(self):
       mehs = Emotion.objects.filter(subject=self.name, attitude_id=2)
       return mehs

    @property
    def haters(self):
       haters = Emotion.objects.filter(subject=self.name, attitude_id=3)
       return haters


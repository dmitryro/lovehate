from django.contrib.auth.models import User
from django.db import models
from datetime import date
from datetime import datetime
from transliterate import translit, get_available_language_codes

class Topic(models.Model):
    name = models.CharField(max_length=250,
                            blank=True,
                            null=True)

    translit_name = models.CharField(max_length=250,
                                     blank=True,
                                     null=True)

    ip_address = models.CharField(max_length=40,
                            blank=True,
                            null=True)

    time_published = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    creator = models.ForeignKey(User,
                                blank=True,
                                null=True,
                                on_delete=models.CASCADE)


    def __str__(self):
        return self.translit_name

    class Meta:
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'

    @property
    def date_time_published(self):
        dt = str(self.time_published)
        year = dt[0:4]
        month = dt[5:7]
        day = dt[8:10]
        return "{}/{}/{} {}:{}:{}".format(day,
                                          month,
                                          year,
                                          self.time_published.hour,
                                          self.time_published.minute,
                                          self.time_published.second)
    @property
    def creator_name(self):
        return self.creator.username



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
        verbose_name_plural = 'Importance'


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

    ip_address = models.CharField(max_length=40,
                            blank=True,
                            null=True)

    time_published = models.DateTimeField(auto_now_add=True)

    time_last_edited = models.DateTimeField(blank=True,
                                            null=True)

    rating =  models.FloatField(default=0, 
                                blank=True, 
                                null=True)

    attitude = models.ForeignKey(Attitude, 
                                 blank=True, 
                                 null=True,
                                 on_delete=models.CASCADE) 

    topic = models.ForeignKey(Topic,
                              blank=True,
                              null=True,
                              related_name='topic',
                              on_delete=models.CASCADE)   

    def __str__(self):
        return self.translit_subject

    @property
    def body_lines(self):
        return self.emotion.splitlines()

    @property
    def date_published(self):
        dt = str(self.time_published)
        year = dt[0:4]
        month = dt[5:7]
        day = dt[8:10]
        return "{}/{}/{}".format(day,
                                 month,
                                 year)

    @property
    def date_time_published(self):
        dt = str(self.time_published)
        year = dt[0:4]
        month = dt[5:7]
        day = dt[8:10]
        return "{}/{}/{} {}:{}:{}".format(day,
                                          month,
                                          year,
                                          self.time_published.hour,
                                          self.time_published.minute,
                                          self.time_published.second)

    @property
    def publishing_user_id(self):
        try:
            return self.user.id
        except Exception as e:
            return -1

    class Meta:
        verbose_name = 'Emotion'
        verbose_name_plural = 'Emotions'



class Message(models.Model):
    subject = models.CharField(max_length=250,
                               blank=True,
                               null=True)

    body = models.TextField(blank=True,
                            null=True)

    is_sent = models.NullBooleanField(default=False, blank=True, null=True)

    is_read = models.NullBooleanField(default=False, blank=True, null=True)

    time_sent = models.DateTimeField(auto_now_add=True)

    sender = models.ForeignKey(User,
                               blank=True,
                               null=True,
                               related_name='sender',
                               on_delete=models.CASCADE)

    receiver =  models.ForeignKey(User,
                                  blank=True,
                                  null=True,
                                  related_name='receiver',
                                  on_delete=models.CASCADE)
    attitude = models.ForeignKey(Attitude,
                                 blank=True,
                                 null=True,
                                 related_name='attitude',
                                 on_delete=models.CASCADE)
    importance = models.IntegerField(default=0)

    ip_address = models.CharField(max_length=40,
                                  blank=True,
                                  null=True)

    @property
    def body_lines(self):
        return self.body.splitlines()

    @property
    def date_time_sent(self):
        dt = str(self.time_sent)
        year = dt[0:4]
        month = dt[5:7]
        day = dt[8:10]
        return "{}/{}/{} {}:{}:{}".format(day,
                                          month,
                                          year,
                                          self.time_sent.hour,
                                          self.time_sent.minute,
                                          self.time_sent.second)

    def __str__(self):
        return self.subject

    @property
    def receiver_name(self):
        return self.receiver.first_name+' '+self.receiver.last_name


    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'


class NotificationType(models.Model):
    notification_type = models.CharField(max_length=50, blank=True, null=True)
    notification_code = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = 'Notification Type'
        verbose_name_plural = 'Notification Types'


class Notification(models.Model):
    is_received = models.NullBooleanField(default=False,
                                          blank=True,
                                          null=True)

    is_sent = models.NullBooleanField(default=False,
                                      blank=True,
                                      null=True)

    message =  models.ForeignKey(Message, 
                                 blank=True, 
                                 null=True,
                                 on_delete=models.CASCADE)

    notification_type = models.ForeignKey(NotificationType,
                                          blank=True, 
                                          null=True,
                                          on_delete=models.CASCADE)

    user = models.ForeignKey(User, blank=True, 
                             null=True,
                             on_delete=models.CASCADE)

    time_sent = models.DateTimeField(auto_now_add=True)

    @property
    def date_time_sent(self):
        dt = str(self.time_sent)
        year = dt[0:4]
        month = dt[5:7]
        day = dt[8:10]
        return "{}/{}/{} {}:{}:{}".format(day,
                                          month,
                                          year,
                                          self.time_sent.hour,
                                          self.time_sent.minute,
                                          self.time_sent.second)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'



class MessagingSettings(models.Model):
    user = models.OneToOneField(User, blank=True, null=True,
                                on_delete=models.CASCADE) 
    duplicate_private = models.NullBooleanField(default=False,
                                                blank=True,
                                                null=True)

    class Meta:
        verbose_name = 'Messaging Settings'
        verbose_name_plural = 'Messaging Settings'

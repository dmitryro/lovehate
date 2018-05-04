from django.db import models
from django.contrib.auth.models import User
from custom.forum.models import Attitude

class Post(models.Model):
    link = models.CharField(max_length=1450, blank=True, null=True)
    author = models.ForeignKey(User, blank=True, null=True,  on_delete=models.CASCADE)
    subject = models.CharField(max_length=1250, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    time_published = models.DateTimeField(auto_now_add=True)
    rating =  models.FloatField(default=0, blank=True, null=True)
    attitude = models.ForeignKey(Attitude, blank=True, null=True, on_delete=models.CASCADE)
    translit_subject = models.CharField(max_length=1250,
                                        blank=True,
                                        null=True)
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'





from django.db import models
from django.contrib.auth.models import User
from custom.forum.models import Attitude
from enumfields import EnumField, Enum

class BlogEmotion(Enum):
    LOVE = 'l'
    NAH = 'n'
    HATE = 'h'

    class Labels:
        MEH = 'A custom label'

class Tempblog(models.Model):
    b_id = models.IntegerField()
    b_ip = models.CharField(max_length=1250, blank=True, null=True)
    b_date = models.DateTimeField(blank=True, null=True)
    uid = models.IntegerField()
    b_subject = models.CharField(max_length=1250, blank=True, null=True)
    b_message = models.CharField(max_length=15250, blank=True, null=True)
    b_emotion = EnumField(BlogEmotion, max_length=1)
    b_delete_mark =  models.IntegerField()
    b_marked_by = models.IntegerField()
    last_edit_time =  models.DateTimeField(blank=True, null=True)






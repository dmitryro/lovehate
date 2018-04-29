from django.db import models

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from datetime import date


class Profile(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250, blank=True, null=True)
    last_name = models.CharField(max_length=250, blank=True, null=True)
    email = models.CharField(max_length=250, blank=True, null=True)
    username = models.CharField(max_length=250, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to='avatars')
    avatar_thumbnail = ImageSpecField(source='avatar',
                                      processors=[ResizeToFill(100, 50)],
                                      format='JPEG',
                                      options={'quality': 60})
    profile_image_path = models.CharField(max_length=250, blank=True, 
                                          null=True, 
                                          default='/media/avatars/default.png')
    title = models.CharField(max_length=250, blank=True, null=True,default='')
    bio = models.TextField(blank=True, null=True,default='') 
    phone = models.CharField(max_length=250, blank=True, null=True,default='')
    is_new = models.NullBooleanField(default=True, blank=True, null=True)
    activation_sent = models.NullBooleanField(default=False, blank=True, null=True)
    is_activated = models.NullBooleanField(default=False, blank=True, null=True)
    is_avatar_processed = models.BooleanField(default=False, blank=True)
    is_avatar_transfered = models.BooleanField(default=False, blank=True)
    is_signature_customized = models.BooleanField(default=False, blank=True)
    is_notification_sent = models.NullBooleanField(default=False, blank=True, null=True)
    is_online = models.BooleanField(default=False, blank=True)
    is_confirmed = models.NullBooleanField(default=False, blank=True, null=True)
    is_cleared = models.BooleanField(default=False, blank=True)
    is_facebook_signup_used = models.BooleanField(default=False, blank=True)
    is_google_signup_used = models.BooleanField(default=False, blank=True)
    is_twitter_signup_used = models.BooleanField(default=False, blank=True)
    is_vk_signup_used = models.BooleanField(default=False, blank=True)
    is_linkedin_signup_used = models.BooleanField(default=False, blank=True)
    is_username_customized = models.BooleanField(default=False, blank=True)
    is_user_avatar = models.BooleanField(default=False, blank=True)
    is_google_avatar = models.BooleanField(default=False, blank=True)
    is_facebook_avatar = models.BooleanField(default=False, blank=True)        
    is_twitter_avatar = models.BooleanField(default=False, blank=True)
    is_vk_avatar = models.BooleanField(default=False, blank=True)
    activation_key =  models.CharField(max_length=250, blank=True, null=True,default='')

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'      

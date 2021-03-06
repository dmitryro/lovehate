from django.contrib import admin
from custom.forum.models import Attitude
from custom.forum.models import Emotion
from custom.forum.models import Topic
from custom.forum.models import Message
from custom.forum.models import NotificationType
from custom.forum.models import Notification


####################################################
# Register Notification Type with Django Admin     #
####################################################

class NotificationTypeAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['notification_type',
                                    'notification_code',]}),)
    list_display = ('id', 'notification_code', 'notification_type',)
    list_editable = ('notification_code', 'notification_type',)
    search_fields = ('notification_code', 'notification_type',)

    class Meta:
         verbose_name = 'Notification Type'
         verbose_name_plural = 'Notification Types'


########################################
# Register Topic with Django Admin     #
########################################

class TopicAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['name',
                                    'translit_name',
                                    'ip_address',
                                    'creator',]}),)
    list_display = ('id', 'name', 'ip_address', 'translit_name', 'creator',)
    list_editable = ('name', 'ip_address', 'translit_name', 'creator',)
    search_fields = ('name', 'ip_address', 'translit_name', 'creator',)

    class Meta:
         verbose_name = 'Topic'
         verbose_name_plural = 'Topics'


########################################
# Register Attitude with Django Admin  #
########################################

class AttitudeAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['name',
                                    'code']}),)
    list_display = ('id', 'name', 'code', )
    list_editable = ('name', 'code',)
    search_fields = ('name', 'code',)

    class Meta:
         verbose_name = 'Attitude'
         verbose_name_plural = 'Attitudes'


class MessageAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['subject', 'body', 'is_sent', 'ip_address', 
                                    'importance', 'attitude', 'sender',  'receiver',]}),)
    list_display = ('id','subject', 'body', 'is_sent', 'is_read', 
                    'importance', 'attitude', 'sender',  'receiver', 'ip_address') 
             #       'sender',  'receiver', 'attitude', 'importance',)
    list_editable = ('subject', 'body', 'is_sent', 'is_read', 'importance',
                     'attitude','sender',  'receiver', 'ip_address',) 
              #       'sender',  'receiver', 'attitude', 'importance',),
    search_fields = ('subject', 'body', 'is_sent', 'is_read', 'importance',
                     'attitude','sender',  'receiver', 'ip_address',) 
              #       'sender',  'receiver', 'attitude', 'importance',)

    class Meta:
         verbose_name = 'Message'
         verbose_name_plural = 'Messages'


########################################
#  Register Emotion with Django Admin  #
########################################

class EmotionAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['user',
                                    'subject',
                                    'translit_subject',
                                    'emotion',
                                    'topic',
                                    'attitude',
                                    'ip_address',
                                    'rating']}),)

    list_display = ('id','user', 'subject', 'topic', 'translit_subject', 
                    'emotion', 'attitude', 'rating', 'ip_address',)
    list_editable = ('user', 'subject', 'topic', 'translit_subject', 
                     'emotion', 'attitude', 'rating', 'ip_address',)
    search_fields = ('user', 'subject', 'topic', 'translit_subject', 
                     'emotion', 'attitude', 'rating', 'ip_address',)

    class Meta:
         verbose_name = 'Emotion'
         verbose_name_plural = 'Emotions'


admin.site.register(NotificationType, NotificationTypeAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Attitude, AttitudeAdmin)
admin.site.register(Emotion, EmotionAdmin)
admin.site.register(Message, MessageAdmin)

from django.contrib import admin
from custom.forum.models import Attitude
from custom.forum.models import Emotion
from custom.forum.models import Topic
from custom.forum.models import Message

########################################
# Register Topic with Django Admin     #
########################################

class TopicAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['name',
                                    'translit_name',
                                    'creator',]}),)
    list_display = ('id', 'name', 'translit_name', 'creator',)
    list_editable = ('name', 'translit_name', 'creator',)
    search_fields = ('name', 'translit_name', 'creator',)

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
    fieldsets = ((None, {'fields': ['subject', 'body', 'is_sent','importance','attitude','sender',  'receiver',]}),)
                      #   'is_read', 'sender',
                      #   'receiver', 'attitude', 'importance',]}),)
    list_display = ('id','subject', 'body', 'is_sent', 'is_read', 'importance', 'attitude',) 
             #       'sender',  'receiver', 'attitude', 'importance',)
    list_editable = ('subject', 'body', 'is_sent', 'is_read', 'importance','attitude','sender',  'receiver',) 
              #       'sender',  'receiver', 'attitude', 'importance',),
    search_fields = ('subject', 'body', 'is_sent', 'is_read',) 
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
                                    'rating']}),)

    list_display = ('id','user', 'subject', 'topic', 'translit_subject', 'emotion', 'attitude', 'rating',)
    list_editable = ('user', 'subject', 'topic', 'translit_subject', 'emotion', 'attitude', 'rating',)
    search_fields = ('user', 'subject', 'topic', 'translit_subject', 'emotion', 'attitude', 'rating',)

    class Meta:
         verbose_name = 'Emotion'
         verbose_name_plural = 'Emotions'


admin.site.register(Topic, TopicAdmin)
admin.site.register(Attitude, AttitudeAdmin)
admin.site.register(Emotion, EmotionAdmin)
admin.site.register(Message, MessageAdmin)

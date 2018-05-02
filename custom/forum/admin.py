from django.contrib import admin
from custom.forum.models import Attitude
from custom.forum.models import Emotion
from custom.forum.models import Topic


########################################
# Register Topic with Django Admin     #
########################################

class TopicAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['name',
                                    'translit_name']}),)
    list_display = ('id', 'name', 'translit_name', )
    list_editable = ('name', 'translit_name',)
    search_fields = ('name', 'translit_name',)

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



########################################
#  Register Emotion with Django Admin  #
########################################

class EmotionAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['user',
                                    'subject',
                                    'translit_subject',
                                    'emotion',
                                    'attitude',
                                    'rating']}),)

    list_display = ('id','user', 'subject', 'translit_subject','emotion', 'attitude', 'rating',)
    list_editable = ('user', 'subject', 'translit_subject', 'emotion', 'attitude', 'rating',)
    search_fields = ('user', 'subject', 'translit_subject', 'emotion', 'attitude', 'rating',)

    class Meta:
         verbose_name = 'Emotion'
         verbose_name_plural = 'Emotions'


admin.site.register(Topic, TopicAdmin)
admin.site.register(Attitude, AttitudeAdmin)
admin.site.register(Emotion, EmotionAdmin)


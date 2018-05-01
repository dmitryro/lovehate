from django.contrib import admin
from custom.forum.models import Attitude
from custom.forum.models import Emotion

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
                                    'emotion',
                                    'attitude',
                                    'rating']}),)

    list_display = ('id','user', 'subject', 'emotion', 'attitude', 'rating',)

    list_editable = ('user', 'subject', 'emotion', 'attitude', 'rating',)
    search_fields = ('user', 'subject', 'emotion', 'attitude', 'rating',)

    class Meta:
         verbose_name = 'Emotion'
         verbose_name_plural = 'Emotions'


admin.site.register(Attitude, AttitudeAdmin)
admin.site.register(Emotion, EmotionAdmin)


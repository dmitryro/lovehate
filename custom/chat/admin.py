from django.contrib import admin
from custom.chat.models import Room
from custom.chat.models import Message
from custom.chat.models import UserChannel

########################################
# Register User Channel with Django    #
########################################

class UserChannelAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['name',
                                    'owner', 'pending_messages',]}),)

    list_display = ('id', 'name', 'owner',)
    list_editable = ('name', 'owner',)
    search_fields = ('name', 'owner',)

    class Meta:
         verbose_name = 'User Channel'
         verbose_name_plural = 'User Channel'


########################################
#  Register Room with Django Admin     #
########################################

class RoomAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['name',
                                    'creator',]}),)
    list_display = ('id', 'name', 'creator',)
    list_editable = ('name', 'creator',)
    search_fields = ('name', 'creator',)

    class Meta:
         verbose_name = 'Room'
         verbose_name_plural = 'Rooms'

########################################
#  Register Message with Django Admin  #
########################################

class MessageAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['body',
                                    'subject',
                                    'sender',
                                    'color', 
                                    'receivers',
                                    'room',]}),)
    list_display = ('id', 'body', 'subject', 'sender', 'room', 'color',)
    list_editable = ('body', 'subject', 'sender', 'room', 'color',)
    search_fields = ('body', 'subject', 'sender', 'room', 'color',)

    class Meta:
         verbose_name = 'Message'
         verbose_name_plural = 'Messages'

admin.site.register(UserChannel, UserChannelAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Message, MessageAdmin)


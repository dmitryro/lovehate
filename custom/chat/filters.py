import rest_framework_filters as filters
import django_filters

from custom.chat.models import Room
from custom.chat.models import Message

#class RoomFilter(filters.FilterSet):
#    class Meta:
#        model = Room
#        fields = {'name': ['exact', 'in', 'startswith'],
#                  'id': ['exact']}

class MessageFilter(filters.FilterSet):
    id = filters.CharFilter(name='id')
    sender_id = filters.CharFilter(name='sender_id')
    room_id = filters.CharFilter(name='room_id')
    receivers = filters.CharFilter(name='receivers')
    time_sent = filters.CharFilter(name='time_sent')
    subject = filters.CharFilter(name='subject')
    body = filters.CharFilter(name='body')

    class Meta:
        model = Message
        fields = ['id', 'subject', 'body', 'room_id', 'sender_id', 'receivers']


class RoomFilter(filters.FilterSet):
    id = filters.CharFilter(name='id')
    name = filters.CharFilter(name='name')
    is_active = filters.CharFilter(name='is_active')
    time_created = filters.CharFilter(name='time_created') 
    creator_id = filters.CharFilter(name='creator_id')

 
    class Meta:
        model = Room
        fields = ['id', 'name', 'is_active', 'time_created', 'creator_id']

import rest_framework_filters as filters
import django_filters

from custom.chat.models import Room
from custom.chat.models import Message
from custom.chat.models import UserChannel

class UserChannelFilter(filters.FilterSet):
    id = filters.CharFilter(name='id')
    owner_id = filters.CharFilter(name='owner_id')
    name = filters.CharFilter(name='name')
    pending_messages = filters.CharFilter(name='pending_messages')
    last_seen = filters.CharFilter(name='last_seen')
    time_created = filters.CharFilter(name='time_created')

    class Meta:
        model = UserChannel
        fields = ['id', 'owner_id', 'name', 'last_seen', 'time_created', 'pending_messages']


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

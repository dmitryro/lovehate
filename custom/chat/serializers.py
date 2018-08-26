from django.contrib.auth.models import User
from rest_framework import serializers
from custom.chat.models import Room
from custom.chat.models import Message
from custom.chat.models import UserChannel

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')



class RoomSerializer(serializers.ModelSerializer):
    creator = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Room
        fields = ('id', 'name', 'time_created', 'creator',)


class MessageSerializer(serializers.ModelSerializer):
    room = RoomSerializer(many=False, read_only=True)
    sender = UserSerializer(many=False, read_only=True)
    receivers = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'body', 'subject', 'sender', 'room', 
                  'is_sent', 'color', 'time_sent', 'sender', 
                  'attitude', 'receivers')


class UserChannelSerializer(serializers.ModelSerializer):
    pending_messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = UserChannel
        fields = ('id', 'name', 'last_seen', 'time_created', 'pending_messages',)



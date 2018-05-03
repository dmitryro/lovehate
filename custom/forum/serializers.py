from custom.forum.models import Emotion
from custom.forum.models import Attitude
from custom.forum.models import Topic
from custom.forum.models import Message
from custom.forum.models import Importance
from custom.forum.models import NotificationType
from custom.forum.models import Notification
from custom.forum.models import MessagingSettings

from rest_framework import serializers
from custom.users.serializers import UserSerializer

class NotificationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationType
        fields = ('id','notification_code','notification_type')


class NotificationSerializer(serializers.ModelSerializer):
    notification_type = NotificationTypeSerializer(many=False, read_only=True)

    class Meta:
        model = Notification
        fields = ('id', 'is_received', 'is_sent', 'message',
                  'notification_type', 'user', 'time_sent')


class MessagingSettingsSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    
    class Meta:
        model = MessagingSettings
        fields = ('id', 'duplicate_private', 'user',)


class AttitudeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attitude
        fields = ('id', 'name', 'code',)


class EmotionSerializer(serializers.ModelSerializer):
    attitude = AttitudeSerializer(many=False, read_only=True)
    class Meta:
        model = Emotion
        fields = ('id', 'user', 'subject', 
                  'feeling', 'rating', 
                  'time_publised', 'subject_translit')

class TopicSerializer(serializers.ModelSerializer):
    creator = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Topic
        fields = ('id', 'name', 'time_created', 'lovers', 'haters', 'mehs', 'creator')

class MessageSerializer(serializers.ModelSerializer):
    attitude = AttitudeSerializer(many=False, read_only=True)
    sender = UserSerializer(many=False, read_only=True)
    receiver = UserSerializer(many=False, read_only=True)
 
    class Meta:
        model = Message
        fields = ('id', 'subject', 'body', 'is_sent', 
                  'is_read', 'time_sent', 'sender', 
                  'receiver', 'attitude', 'importance',)


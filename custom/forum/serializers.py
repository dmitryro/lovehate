from custom.forum.models import Emotion
from custom.forum.models import Attitude
from custom.forum.models import Topic
from custom.forum.models import Message
from custom.forum.models import Importance
from rest_framework import serializers
from custom.users.serializers import UserSerializer

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


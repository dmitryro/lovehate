from custom.forum.models import Emotion
from custom.forum.models import Attitude
from custom.forum.models import Topic
from rest_framework import serializers

class AttitudeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attitude
        fields = ('id', 'name', 'code',)

class EmotionSerializer(serializers.ModelSerializer):
    attitude = AttitudeSerializer(many=False,read_only=True)
    class Meta:
        model = Emotion
        fields = ('id', 'user', 'subject', 
                  'feeling', 'rating', 
                  'time_publised', 'subject_translit')

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('id', 'name', 'time_created', 'lovers', 'haters', 'mehs',)

from custom.forum.models import Emotion
from custom.forum.models import Attitude
from rest_framework import serializers

class AttitudeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attitude
        fields = ('id', 'name', 'code',)


class EmotionSerializer(serializers.ModelSerializer):
    attitude = AttitudeSerializer(many=False,read_only=True)
    class Meta:
        model = Emotion
        fields = ('id', 'user', 'subject', 'feeling', 'rating', 'time_publised',)


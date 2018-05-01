from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework import generics
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework import exceptions

from custom.users.signals import user_resend_activation
from custom.users.serializers import UserSerializer
from custom.users.callbacks import resend_activation_handler
from custom.users.models import Profile
from custom.utils.models import Logger
from custom.forum.models import Emotion
from custom.forum.models import Attitude
from custom.forum.serializers import AttitudeSerializer
from custom.forum.serializers import EmotionSerializer


class AttitudeList(generics.ListAPIView):
    queryset = Attitude.objects.all()
    serializer_class = AttitudeSerializer

class AttitudeDetail(generics.RetrieveAPIView):
    queryset = Attitude.objects.all()
    serializer_class = AttitudeSerializer

class EmotionList(generics.ListAPIView):
    queryset = Emotion.objects.all()
    serializer_class = EmotionSerializer

class EmotionDetail(generics.RetrieveAPIView):
    queryset = Emotion.objects.all()
    serializer_class = EmotionSerializer

class EmotionViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing attitude instances.
    """
    serializer_class = EmotionSerializer
    queryset = Emotion.objects.all()


def forum_new(request):
    redirect = 'forum_new.html'

    log = Logger(log='USER IS AUTHENTICATED {}'.format(request.user.is_authenticated))
    log.save()

    try:
        if request.user.is_authenticated:
            logout=True
            user_id = request.user.id
            username = request.user.username
            is_authenticated = True
        else:
            logout=False
            user_id = -1
            username = ''
            is_authenticated = False
    except Exception as e:
            username = ''
            logout=False
            user_id = -1
            is_authenticated = False

    log = Logger(log='USER IS AUTHENTICATED {} username {}'.format(request.user.is_authenticated, username))
    log.save()

    return render(request, redirect,{'home':'forum_new.html',
                                     'user': request.user,
                                     'username': username,
                                     'is_authenticated': is_authenticated,
                                     'current_page': 'new_feeling',
                                     'username': request.user.username,
                                     'logout': False})


@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def newemotion(request):
    try:
        emotion = request.data.get('emotion', '')
        subject = request.data.get('subject', '')
        attitude = int(request.data.get('attitude', None))
        user_id = int(request.data.get('user_id', None))
        attitude = Attitude.objects.get(id=attitude)

        user = User.objects.get(id=user_id)

        em = Emotion.objects.get(subject=subject)

        if not em:
            em = Emotion.objects.get(subject=subject.lower())

        if not em:
            Emotion.objects.create(user=user, attitude=attitude, emotion=emotion, subject=subject)
        else:
            Emotion.objects.create(user=user, attitude=attitude, emotion=emotion, subject=em.subject)

    except Exception as e:
        return Response({"message": "failed - {}".format(e),
                         "status": "posted",
                         "code": 400,
                         "falure_code": 1}, status=200)

    return Response({"message": "success - username used",
                     "status": "posted",
                     "code": 200,
                     "falure_code": 0}, status=200)


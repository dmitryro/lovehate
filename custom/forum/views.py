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

from transliterate import translit, get_available_language_codes
from transliterate import detect_language

from custom.users.signals import user_resend_activation
from custom.users.serializers import UserSerializer
from custom.users.callbacks import resend_activation_handler
from custom.users.models import Profile
from custom.utils.models import Logger
from custom.forum.models import Emotion
from custom.forum.models import Attitude
from custom.forum.models import Topic
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


def topics(request, topic_id):
    redirect = 'topics.html'
    try:
        lovers = Emotion.objects.filter(attitude_id=1, topic_id=topic_id)
        mehs = Emotion.objects.filter(attitude_id=2, topic_id=topic_id)
        haters = Emotion.objects.filter(attitude_id=3, topic_id=topic_id)
        log = Logger(log="TOPICS DID READ {} {} {}".format(lovers, mehs, haters))
        log.save()
    
 
    except Exception as e:
        log = Logger(log="TOPICS DID NOT READ {}".format(e))
        log.save()
        lovers = []
        mehs = []
        haters = []

    log = Logger(log="EMPTIONS BEFORE WE RENDER lovers {} mehs {} haters {}".format(lovers, mehs, haters))
    log.save()

    if request.user:
        if request.user.is_authenticated:
            username = request.user.username
        else:
            username = ''
    else:
        username = ''

    return render(request, redirect,{'home':'topics.html',
                                     'lovers': lovers,
                                     'mehs' : mehs,
                                     'haters': haters,
                                     'username': username,
                                     'user_id': request.user.id,
                                     'user': request.user,
                                     'current_page': 'topics',
                                     'logout': False})

def forum_new(request):
    redirect = 'forum_new.html'

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

    return render(request, redirect,{'home':'forum_new.html',
                                     'user': request.user,
                                     'username': username,
                                     'is_authenticated': is_authenticated,
                                     'current_page': 'new_feeling',
                                     'username': request.user.username,
                                     'logout': False})

def outgoing_messages(request):
    redirect = 'outgoing.html'

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

    return render(request, redirect,{'home':'outgoing.html',
                                     'user': request.user,
                                     'username': username,
                                     'is_authenticated': is_authenticated,
                                     'current_page': 'outgoing',
                                     'username': request.user.username,
                                     'logout': False})


def incoming_messages(request):
    redirect = 'incoming.html'

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

    return render(request, redirect,{'home':'incoming.html',
                                     'user': request.user,
                                     'username': username,
                                     'is_authenticated': is_authenticated,
                                     'current_page': 'incoming',
                                     'username': request.user.username,
                                     'logout': False})


@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def newmessage(request):
    try:

        message = request.data.get('message', '')
        subject = request.data.get('subject', '')
        recipients = request.data.get('recipients', '')
        attitude = int(request.data.get('attitude', None))
        sender_id = int(request.data.get('sender_id', None))
        attitude = Attitude.objects.get(id=attitude)
        trans_subject = translit(str(subject), reversed=True)
        message = "Message: {}, Subject: {}, Recipients: {}, Attitude: {}, Sender ID {} trans {}"
        message = message.format(message,
                                 subject,
                                 recipient,
                                 attitude,
                                 sender_id,
                                 trans_subject)
        log = Logger(log=message)
        log.save()        
    except Exception as e:
        log = Logger(log="This just didn't work {}".format(e))
        log.save()         


    return Response({"message": "success - message sent",
                     "status": "posted",
                     "code": 200,
                     "falure_code": 0}, status=200)


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

        try:
            language = detect_language(str(subject))
        except Exception as e:
            language = 'en'

        log = Logger(log="LANGUAGE WAS {}".format(language))
        log.save()

        if language=='ru':
            trans_subject = translit(str(subject), reversed=True) 
        elif language=='he':
            trans_subject = translit(str(subject), reversed=True)
        elif language=='jp': 
            trans_subject = translit(str(subject), reversed=True)
        else:
            trans_subject = str(subject).lower()

        try:
            topic = Topic.objects.get(translit_name=trans_subject)
        except Exception as e:
            topic = Topic.objects.create(name=subject, 
                                         translit_name=trans_subject)
                     

        user = User.objects.get(id=user_id)
        Emotion.objects.create(user=user, topic=topic, attitude=attitude, emotion=emotion, subject=subject, translit_subject=trans_subject)
        

    except Exception as e:
        log = Logger(log="This just did not work out - failed to create a new topic {}".format(e))
        log.save()

        return Response({"message": "failed - {}".format(e),
                         "status": "posted",
                         "code": 400,
                         "falure_code": 1}, status=200)

    return Response({"message": "success - username used",
                     "status": "posted",
                     "code": 200,
                     "falure_code": 0}, status=200)


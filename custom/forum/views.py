from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

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
from ipware import get_client_ip
from django.utils import timezone
from datetime import datetime
from pytz import timezone as pytz

tz = pytz('Europe/Moscow')


from custom.users.signals import user_resend_activation
from custom.users.serializers import UserSerializer
from custom.users.callbacks import resend_activation_handler
from custom.users.models import Profile
from custom.utils.models import Logger
from custom.forum.models import Emotion
from custom.forum.models import Attitude
from custom.forum.models import Topic
from custom.forum.models import Message
from custom.forum.models import Notification
from custom.forum.models import NotificationType
from custom.forum.serializers import AttitudeSerializer
from custom.forum.serializers import EmotionSerializer
from custom.forum.signals import message_read
from custom.forum.signals import message_sent
from custom.forum.signals import message_deleted
from custom.forum.signals import message_updated
from custom.forum.signals import message_duplicate_to_email
from custom.forum.callbacks import message_deleted_handler
from custom.forum.callbacks import message_read_handler
from custom.forum.callbacks import message_sent_handler
from custom.forum.callbacks import message_updated_handler
from custom.forum.callbacks import message_duplicate_to_email_handler
from custom.forum.serializers import MessageSerializer
from custom.forum.serializers import MessagingSettingsSerializer
from custom.forum.serializers import NotificationSerializer
from custom.forum.serializers import NotificationTypeSerializer
from custom.users.serializers import UserSerializer

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
        has_private = request.user.profile.has_private
    except Exception as e:
        has_private = False

    try:
        lovers = Emotion.objects.filter(attitude_id=1, topic_id=topic_id).order_by('-time_last_edited')
    except Exception as e:
       lovers = []

    try:
        mehs = Emotion.objects.filter(attitude_id=2, topic_id=topic_id).order_by('-time_last_edited')
    except Exception as e:
        mehs = []
 
    try:
        haters = Emotion.objects.filter(attitude_id=3, topic_id=topic_id).order_by('-time_last_edited')
    except Exception as e:
        haters = []
    
    try:
        topic = Topic.objects.get(id=int(topic_id))
    except Exception as e:
        topic = None
        log = Logger(log="TOPICS DID NOT READ {}".format(e))
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
                                     'topic': topic,
                                     'mehs' : mehs,
                                     'has_private': has_private,
                                     'haters': haters,
                                     'username': username,
                                     'user_id': request.user.id,
                                     'user': request.user,
                                     'current_page': 'topics',
                                     'logout': False})

def forum_new(request):

    try:
        has_private = request.user.profile.has_private
    except Exception as e:
        has_private = False

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

    if request.user.is_authenticated:
        redirect = 'forum_new.html'
    else:
        redirect = 'forum_new_unauth.html'

    return render(request, redirect,{'home':'forum_new.html',
                                     'user': request.user,
                                     'username': username,
                                     'is_authenticated': is_authenticated,
                                     'current_page': 'new_feeling',
                                     'has_private': has_private,
                                     'username': request.user.username,
                                     'logout': False})

def forum_add(request, topic_id, attitude_id):
    try:
        has_private = request.user.profile.has_private
    except Exception as e:
        has_private = False


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

    try:
        attitude = Attitude.objects.get(id=int(attitude_id))
    except Exception as e:
        attitude = Attitude.objects.get(id=3)

    try:
        topic = Topic.objects.get(id=int(topic_id))
    except Exception as e:
        topic = None

    if is_authenticated:
        redirect = 'forum_add.html'
    else:
        redirect = 'forum_add_unauth.html'

    return render(request, redirect,{'home':'forum_new.html',
                                     'user': request.user,
                                     'username': username,
                                     'attitude': attitude,
                                     'has_private': has_private,
                                     'topic': topic,
                                     'is_authenticated': is_authenticated,
                                     'current_page': 'new_feeling',
                                     'username': request.user.username,
                                     'logout': False})


def forum_edit(request, topic_id, emotion_id):
    try:
        has_private = request.user.profile.has_private
    except Exception as e:
        has_private = False


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

    try:
        emotion = Emotion.objects.get(id=int(emotion_id))
    except Exception as e:
        amotion = None

    try:
        topic = Topic.objects.get(id=int(topic_id))
    except Exception as e:
        topic = None

    redirect = 'forum_edit.html'

    return render(request, redirect,{'home':'forum_new.html',
                                     'user': request.user,
                                     'username': username,
                                     'emotion': emotion,
                                     'has_private': has_private,
                                     'topic': topic,
                                     'is_authenticated': is_authenticated,
                                     'current_page': 'new_feeling',
                                     'username': request.user.username,
                                     'logout': False})



def outgoing_messages(request):
    redirect = 'outgoing.html'

    try:
        has_private = request.user.profile.has_private
    except Exception as e:
        has_private = False


    try:
        delete_ids = request.POST.getlist('outgoing_delete')

        for delete_id in delete_ids:
            message = Message.objects.get(id=int(delete_id))
            message.delete()
    except Exception as e:
        log = Logger(log='Could not delete {}'.format(e))
        log.save()

    page = request.GET.get('page', 1)

    try:
        if request.user.is_authenticated:
            logout=True
            user_id = request.user.id
            username = request.user.username
            is_authenticated = True
            outgoing = Message.objects.filter(sender_id=user_id).order_by('-time_sent')
        else:
            logout=False
            user_id = -1
            username = ''
            is_authenticated = False
            outgoing = []
    except Exception as e:
            username = ''
            logout=False
            user_id = -1
            is_authenticated = False
            outgoing = []

    paginator = Paginator(outgoing, 10)

    try:
        outgoing_slice = paginator.page(page)
    except PageNotAnInteger:
        outgoing_slice = paginator.page(1)
    except EmptyPage:
        outgoing_slice = paginator.page(paginator.num_pages)


    return render(request, redirect,{'home':'outgoing.html',
                                     'user': request.user,
                                     'username': username,
                                     'outgoing': outgoing_slice,
                                     'has_private': has_private,
                                     'is_authenticated': is_authenticated,
                                     'current_page': 'outgoing',
                                     'username': request.user.username,
                                     'logout': False})


def incoming_user_messages(request, sender_id):
    redirect = 'incoming_user.html'
    page = request.GET.get('page', 1)

    try:
        has_private = request.user.profile.has_private
    except Exception as e:
        has_private = False

    try:
        delete_ids = request.POST.getlist('incoming_delete')
        for delete_id in delete_ids:
            message = Message.objects.get(id=int(delete_id))
            message.delete()
    except Exception as e:
        pass

    try:
        if request.user.is_authenticated:
            logout=True
            user_id = request.user.id
            username = request.user.username
            is_authenticated = True
            sender_id = int(sender_id)
            sender = User.objects.get(id=sender_id)
            user = request.user
            allmessages = Message.objects.filter(Q(receiver_id=sender_id, sender_id=user_id) | 
                                                 Q(receiver_id=user_id, sender_id=sender_id)).order_by('-time_sent')

            incoming_unread = Message.objects.filter(receiver_id=user_id, is_read=False).order_by('-time_sent')

            if len(incoming_unread) > 0:
                has_private = True
        else:
            logout=False
            user_id = -1
            username = ''
            is_authenticated = False
            all = []
            has_private = False
    except Exception as e:
        username = ''
        logout=False
        user_id = -1
        has_private = False
        is_authenticated = False
        allmessages = []

    paginator = Paginator(allmessages, 10)

    try:
        allmessages_slice = paginator.page(page)
    except PageNotAnInteger:
        allmessages_slice = paginator.page(1)
    except EmptyPage:
        allmessages_slice = paginator.page(paginator.num_pages)

    return render(request, redirect,{'home':'incoming_user.html',
                                     'user': request.user,
                                     'username': username,
                                     'has_private': has_private,
                                     'back_to_user': True,
                                     'allmessages': allmessages_slice,
                                     'is_authenticated': is_authenticated,
                                     'current_page': 'incoming',
                                     'username': request.user.username,
                                     'logout': False})




def incoming_messages(request):
    redirect = 'incoming.html'
    page = request.GET.get('page', 1)

    try:
        has_private = request.user.profile.has_private
    except Exception as e:
        has_private = False

    try:
        delete_ids = request.POST.getlist('incoming_delete')
        for delete_id in delete_ids:
            message = Message.objects.get(id=int(delete_id))
            message.delete()
    except Exception as e:
        pass 

    try:
        if request.user.is_authenticated:
            logout=True
            user_id = request.user.id
            username = request.user.username
            is_authenticated = True
            incoming = Message.objects.filter(receiver_id=user_id).order_by('-time_sent')
            incoming_unread = Message.objects.filter(receiver_id=user_id, is_read=False).order_by('-time_sent')
            if len(incoming_unread) > 0:
                has_private = True
        else:
            logout=False
            user_id = -1
            username = ''
            is_authenticated = False
            incoming = []
            has_private = False
    except Exception as e:
            username = ''
            logout=False
            user_id = -1
            has_private = False
            is_authenticated = False
            incoming = []

    paginator = Paginator(incoming, 10)

    try:
        incoming_slice = paginator.page(page)
    except PageNotAnInteger:
        incoming_slice = paginator.page(1)
    except EmptyPage:
        incoming_slice = paginator.page(paginator.num_pages)

    return render(request, redirect,{'home':'incoming.html',
                                     'user': request.user,
                                     'username': username,
                                     'has_private': has_private,
                                     'incoming': incoming_slice,
                                     'back_to_user': False,
                                     'is_authenticated': is_authenticated,
                                     'current_page': 'incoming',
                                     'username': request.user.username,
                                     'logout': False})

def get_substring_index(orig, search):
    for i, s in enumerate(search):
       if orig in s and len(orig) < len(s):
           return i
    return -1

@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def newmessage(request):
    ip, is_routable = get_client_ip(request)
    ip_address = str(ip)

    try:

        body = request.data.get('message', '')
        subject = request.data.get('subject', '')
        recipients = request.data.get('recipients', '')
        attitude = int(request.data.get('attitude', None))
        sender_id = int(request.data.get('sender_id', None))
        attitude = Attitude.objects.get(id=attitude)

        try:
            language = detect_language(str(subject))
        except Exception as e:
            language = 'en'

        if language=='ru':
            trans_subject = translit(str(subject), reversed=True)
        elif language=='he':
            trans_subject = translit(str(subject), reversed=True)
        elif language=='jp':
            trans_subject = translit(str(subject), reversed=True)
        else:
            trans_subject = str(subject).lower()

        
        receivers = list(set(recipients.split(',')))       

        for i, receiver in enumerate(receivers):
            receivers[i] = receiver.strip()

        
        #receiver = User.objects.get(id=receiver_id)
        sender = User.objects.get(id=sender_id)

        recipients = User.objects.filter(username__in=receivers)
        for receiver in recipients:
            message = Message.objects.create(subject=subject,
                                             attitude=attitude,
                                             importance=1,
                                             body=body,
                                             ip_address=ip_address,
                                             sender=sender,
                                             receiver=receiver)
            if message:
                message_sent.send(sender = sender,
                                  receiver = receiver,
                                  message = message,
                                  kwargs = None)

            log = Logger(log="MESSAGE SENT {}".format(message))
            log.save()        
    except Exception as e:
        log = Logger(log="This just didn't work {}".format(e))
        log.save()         

        return Response({"message": "failure - message was not sent {}".format(e),
                         "status": "posted",
                         "code": 400,
                         "falure_code": 0}, status=400)


    return Response({"message": "success - message sent",
                     "status": "posted",
                     "code": 200,
                     "falure_code": 0}, status=200)


@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def newmessage_unauth(request):
    ip, is_routable = get_client_ip(request)
    ip_address = str(ip)

    try:

        body = request.data.get('message', '')
        subject = request.data.get('subject', '')
        recipients = request.data.get('recipients', '')
        attitude = int(request.data.get('attitude', None))

        attitude = Attitude.objects.get(id=attitude)
        username = request.data.get('username', '')
        password = request.data.get('password', '')


        user = authenticate(username=username, password=password)
        log = Logger(log="AFTER WE TRIED {} {} {}".format(user, username, password))
        log.save()

        if not user:
            return Response({"message": "failed to authenticate",
                             "status": "posted",
                             "code": 400,
                             "falure_code": 2}, status=400)


        login(request, user, backend='custom.users.backends.LocalBackend') #the user is now logged in    
   
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            return Response({"message": 'failure',
                             "code":400,
                             "log_out": False,
                             "status": "unauthenticated",
                             "not_activated": False,
                             "reason": "Invalid user"},
                             status=400)
        #request.session.set_expiry(1086400) #sets the exp. value of the session
        sender_id = user.id

        log = Logger(log="SO FAR SO GOOD {}".format(user, user.is_authenticated))
        log.save()

        try:
            language = detect_language(str(subject))
        except Exception as e:
            language = 'en'

        if language=='ru':
            trans_subject = translit(str(subject), reversed=True)
        elif language=='he':
            trans_subject = translit(str(subject), reversed=True)
        elif language=='jp':
            trans_subject = translit(str(subject), reversed=True)
        else:
            trans_subject = str(subject).lower()


        receivers = list(set(recipients.split(',')))

        for i, receiver in enumerate(receivers):
            receivers[i] = receiver.strip()

        #receiver = User.objects.get(id=receiver_id)
        sender = User.objects.get(id=sender_id)

        recipients = User.objects.filter(username__in=receivers)
        for receiver in recipients:
            message = Message.objects.create(subject=subject,
                                             attitude=attitude,
                                             importance=1,
                                             body=body,
                                             ip_address=ip_address,
                                             sender=sender,
                                             receiver=receiver)
            if message:
                message_sent.send(sender = sender,
                                  receiver = receiver,
                                  message = message,
                                  kwargs = None)

            log = Logger(log="MESSAGE SENT {}".format(message))
            log.save()
    except Exception as e:
        log = Logger(log="This just didn't work {}".format(e))
        log.save()

        return Response({"message": "failure - message was not sent {}".format(e),
                         "status": "posted",
                         "code": 400,
                         "falure_code": 0}, status=400)


    return Response({"message": "success - message sent",
                     "status": "posted",
                     "code": 200,
                     "falure_code": 0}, status=200)





@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def newemotion_unauth(request):
    ip, is_routable = get_client_ip(request)
    ip_address = str(ip)

    try:
        emotion = request.data.get('emotion', '')
        subject = request.data.get('subject', '')
        att = int(request.data.get('attitude', None))
        attitude = Attitude.objects.get(id=int(att))
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        user = authenticate(username=username, password=password)
        if not user:
            return Response({"message": "failed to authenticate",
                             "status": "posted",
                             "code": 400,
                             "falure_code": 2}, status=400)


        login(request, user, backend='custom.users.backends.LocalBackend') #the user is now logged in

        try:
            language = detect_language(str(subject))
        except Exception as e:
            language = 'en'

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
                                         ip_address=ip_address,
                                         creator=user,
                                         translit_name=trans_subject)

        log = Logger(log="TOPIC WAS {}".format(topic))
        log.save()

        Emotion.objects.create(user=user, topic=topic, attitude=attitude,
                               emotion=emotion, subject=subject,
                               ip_address=ip_address,
                               translit_subject=trans_subject)

    except Exception as e:
        log = Logger(log="UNAUTH FAILED - just did not work out - failed to create a new emotion {}".format(e))
        log.save()

        return Response({"message": "failed - {}".format(e),
                         "status": "posted",
                         "code": 400,
                         "falure_code": 1}, status=400)

    return Response({"message": "success - username used",
                     "status": "posted",
                     "code": 200,
                     "falure_code": 0}, status=200)

@csrf_exempt
def read_all_private(request, message_id):
    has_private = False

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

    try:
        message = Message.objects.get(id=int(message_id))
        message.is_read=True
        message.save()
        return render(request, 'read_private.html',{'home':'read_private.html',
                                                      'answer_subject': "RE: {}".format(message.subject),
                                                      'user': request.user,
                                                      'message': message,
                                                      'recipient': message.sender,
                                                      'username': username,
                                                      'has_private': True,
                                                      'current_page': 'private',
                                                      'back_to_user': False,
                                                      'is_authenticated': is_authenticated,
                                                      'logout': logout,
                                                      'user_id': user_id})
    except Exception as e:
        log = Logger(log="SOME SHIT WENT WRONG = 1 {}".format(e))
        log.save()
        return render(request, 'private.html',{'home':'private.html',
                                         'user': request.user,
                                         'username': username,
                                         'has_private': True,
                                         'current_page': 'private',
                                         'is_authenticated': is_authenticated,
                                         'logout': logout,
                                         'user_id': user_id})

@csrf_exempt
def read_private(request, message_id):

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

    try:
        message = Message.objects.get(id=int(message_id))
        message.is_read=True
        message.save()
        return render(request, 'read_private.html',{'home':'read_private.html',
                                                      'answer_subject': "RE: {}".format(message.subject),
                                                      'user': request.user,
                                                      'message': message,
                                                      'has_private': request.user.profile.has_private,
                                                      'recipient': message.sender,
                                                      'username': username,
                                                      'back_to_user': True,
                                                      'current_page': 'private',
                                                      'is_authenticated': is_authenticated,
                                                      'logout': logout,
                                                      'user_id': user_id})
    except Exception as e:
        log = Logger(log="SOME SHIT WENT WRONG = 2 {}".format(e))
        log.save()

        return render(request, 'private.html',{'home':'private.html',
                                         'user': request.user,
                                         'username': username,
                                         'has_private': False,
                                         'current_page': 'private',
                                         'is_authenticated': is_authenticated,
                                         'logout': logout,
                                         'user_id': user_id})


@csrf_exempt
def answer_all_private(request, message_id):
    has_private = True
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

    try:
        message = Message.objects.get(id=int(message_id))
        message.is_read=True
        message.save()
        return render(request, 'answer_private.html',{'home':'answer_private.html',
                                                      'answer_subject': "RE: {}".format(message.subject),
                                                      'user': request.user,
                                                      'has_private': request.user.profile.has_private,
                                                      'recipient': message.sender,
                                                      'back_to_user': False,
                                                      'username': username,
                                                      'current_page': 'private',
                                                      'is_authenticated': is_authenticated,
                                                      'logout': logout,
                                                      'user_id': user_id})
    except Exception as e:
        return render(request, 'private.html',{'home':'private.html',
                                         'user': request.user,
                                         'username': username,
                                         'has_private': has_private,
                                         'current_page': 'private',
                                         'is_authenticated': is_authenticated,
                                         'logout': logout,
                                         'user_id': user_id})



@csrf_exempt
def answer_private(request, message_id):

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

    try:
        message = Message.objects.get(id=int(message_id))
        message.is_read=True
        message.save()
        return render(request, 'answer_private.html',{'home':'answer_private.html',
                                                      'answer_subject': "RE: {}".format(message.subject),
                                                      'user': request.user,
                                                      'has_private': request.user.profile.has_private,
                                                      'recipient': message.sender,
                                                      'username': username,
                                                      'back_to_user': True,
                                                      'current_page': 'private',
                                                      'is_authenticated': is_authenticated,
                                                      'logout': logout,
                                                      'user_id': user_id}) 
    except Exception as e:
        return render(request, 'private.html',{'home':'private.html',
                                         'user': request.user,
                                         'username': username,
                                         'has_private': has_private,
                                         'current_page': 'private',
                                         'is_authenticated': is_authenticated,
                                         'logout': logout,
                                         'user_id': user_id})

@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def editemotion(request):

    ip, is_routable = get_client_ip(request)
    ip_address = str(ip)

    try:
        feeling = request.data.get('feeling', '')
        emotion_id =  int(request.data.get('emotion_id', None))
        subject = request.data.get('subject', '')
        att = int(request.data.get('attitude', None))
        user_id = int(request.data.get('user_id', None))
        attitude = Attitude.objects.get(id=int(att))
        
        log = Logger(log="SO FAR FEELIGN {} EMOTION ID {} SUBJ {} ATT {} USER ID {} ATTRIBUTE {}".format(feeling, emotion_id, subject, att, user_id, attitude))
        log.save()
    
        emotion = Emotion.objects.get(id=emotion_id)

        if not emotion:
            return Response({"message": "failed",
                             "status": "posted",
                             "code": 400,
                             "falure_code": 1}, status=400)
             
        feeling = feeling.strip('')
        feeling = feeling.strip('\t')

        if not feeling or len(feeling) < 1:
            emotion.delete()
            return Response({"message": "success - deleted",
                             "status": "posted",
                             "code": 200,
                             "falure_code": 0}, status=200)

        try:
            language = detect_language(str(subject))
        except Exception as e:
            language = 'en'

        if language=='ru':
            trans_subject = translit(str(subject), reversed=True)
        elif language=='he':
            trans_subject = translit(str(subject), reversed=True)
        elif language=='jp':
            trans_subject = translit(str(subject), reversed=True)
        else:
            trans_subject = str(subject).lower()

        user = User.objects.get(id=user_id)

        try:
            topic = Topic.objects.get(translit_name=trans_subject)
        except Exception as e:
            topic = Topic.objects.create(name=subject,
                                         ip_address=ip_address,
                                         creator=user,
                                         translit_name=trans_subject)
        emotion.time_last_edited = timezone.now().replace(tzinfo=tz)
        emotion.topic = topic
        emotion.emotion = feeling
        emotion.attitude = attitude
        emotion.subject = subject
        emotion.translit_subject = trans_subject
        emotion.save()
    except Exception as e:
        log = Logger(log="This just did not work out - failed to create a new topic {}".format(e))
        log.save()

        return Response({"message": "failed - {}".format(e),
                         "status": "posted",
                         "code": 400,
                         "falure_code": 1}, status=400)

    return Response({"message": "success - username used",
                     "status": "posted",
                     "code": 200,
                     "falure_code": 0}, status=200)



@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def newemotion(request):

    ip, is_routable = get_client_ip(request)
    ip_address = str(ip)

    try:
        emotion = request.data.get('emotion', '')
        subject = request.data.get('subject', '')
        att = int(request.data.get('attitude', None))
        user_id = int(request.data.get('user_id', None))
        attitude = Attitude.objects.get(id=int(att))

        try:
            language = detect_language(str(subject))
        except Exception as e:
            language = 'en'

        if language=='ru':
            trans_subject = translit(str(subject), reversed=True) 
        elif language=='he':
            trans_subject = translit(str(subject), reversed=True)
        elif language=='jp': 
            trans_subject = translit(str(subject), reversed=True)
        else:
            trans_subject = str(subject).lower()

        user = User.objects.get(id=user_id)
        try:
            topic = Topic.objects.get(translit_name=trans_subject)
        except Exception as e:
            topic = Topic.objects.create(name=subject,
                                         ip_address=ip_address,
                                         creator=user, 
                                         translit_name=trans_subject)
                     

        Emotion.objects.create(user=user, topic=topic, attitude=attitude, 
                               emotion=emotion, subject=subject, 
                               ip_address=ip_address,
                               translit_subject=trans_subject)
        

    except Exception as e:
        log = Logger(log="This just did not work out - failed to create a new topic {}".format(e))
        log.save()

        return Response({"message": "failed - {}".format(e),
                         "status": "posted",
                         "code": 400,
                         "falure_code": 1}, status=400)

    return Response({"message": "success - username used",
                     "status": "posted",
                     "code": 200,
                     "falure_code": 0}, status=200)


message_duplicate_to_email.connect(message_duplicate_to_email_handler)
message_read.connect(message_read_handler)
message_sent.connect(message_sent_handler)
message_deleted.connect(message_deleted_handler)
message_updated.connect(message_updated_handler)

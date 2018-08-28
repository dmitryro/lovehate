from django.shortcuts import render
import cyrtranslit
from datetime import timedelta

from online_users.models import OnlineUserActivity
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import logout as log_out
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from custom.utils.models import Logger
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth import authenticate
from django.conf import settings

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework import generics


from custom.forum.models import Emotion
from custom.forum.models import Topic
from custom.blog.models import Post
from custom.chat.models import Room
from custom.chat.models import Message
from custom.chat.models import UserChannel
from custom.chat.signals import user_joined_chat
from custom.chat.signals import user_left_chat
from custom.chat.signals import chat_room_created
from custom.chat.signals import chat_room_terminated
from custom.chat.signals import user_joined_room
from custom.chat.signals import user_left_room
from custom.chat.serializers import RoomSerializer
from custom.chat.serializers import MessageSerializer
from custom.chat.serializers import UserChannelSerializer
from custom.chat.filters import MessageFilter
from custom.chat.filters import RoomFilter
from custom.chat.filters import UserChannelFilter
from custom.utils.models import Logger

#from custom.chat.callbacks import user_joined_chat_handler
#from custom.chat.callbacks import user_left_chat_handler
#from custom.chat.callbacks import user_joined_room_handler
#from custom.chat.callbacks import user_left_room_handler
#from custom.chat.callbacks import chat_room_created_handler
#from custom.chat.callbacks import chat_room_terminated_handler

class RoomsList(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend,)
    filter_class = RoomFilter
    search_fields = ('id', 'name', 'is_active'
                     'date_created', 'creator_id', 
                     'active_users')


class MessagesList(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend,)
    filter_class = MessageFilter
    search_fields = ('id', 'sender_id', 'room_id'
                     'body', 'subject',)


class UserChannelsList(generics.ListAPIView):
    queryset = UserChannel.objects.all()
    serializer_class = UserChannelSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend,)
    filter_class = UserChannelFilter
    search_fields = ('id', 'owner_id', 'name'
                     'last_seen', 'time_created', 
                     'pending_messages',)
    

class RoomViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing chat rooms
    """
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
    filter_fields = ('id', 'name', 'is_active', 'time_created', 'creator_id',)


class MessageViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing chat messages
    """
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    filter_fields = ('id', 'sender_id', 'room_id', 'body', 'subject')   


@csrf_exempt
def display_chat(request):
    try:
        if request.user.is_authenticated:
            logout=True
            user_id = request.user.id
            username = request.user.username
            is_authenticated = True
            has_private = request.user.profile.has_private
        else:
            logout=False
            user_id = -1
            username = ''
            is_authenticated = False
            has_private = False
            return HttpResponseRedirect('/')
        users = User.objects.all()
        rooms = Room.objects.all()

        if len(rooms)==0:
           root = User.objects.get(id=1)
           room = Room.objects.create(name="Курилка", 
                                      creator=root)
           rooms.append(room)

    except Exception as e:
        username = ''
        logout=False
        user_id = -1
        is_authenticated = False
        has_private = False
        users = [] 
        rooms = []
    return render(request, 'chat.html',{'home': 'chat.html',
                                        'user': request.user,
                                        'users': users,
                                        'rooms': rooms,
                                        'chat_user_id': user_id,
                                        'has_private': has_private,
                                        'username': username,
                                        'current_page': 'chat',
                                        'is_authenticated': is_authenticated,
                                        'logout': logout,
                                        'user_id': user_id})



@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def read_rooms(request):
    rooms = Room.objects.all()
    return Response({'message':'success'})


@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def create_room(request):
    return Response({'message':'success'})


@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def join_room(request):
    try:
        user_id = request.data.get('user_id')
        room_id = request.data.get('room_id')
        user = User.objects.get(id=int(user_id))         

        rooms = Room.objects.all()
        
        for room in rooms:
            if room.id == int(room_id):
               room.active_users.remove(user)
               if user in room.active_users.all():  
                   pass
               else:
                   room.active_users.add(user)
            else:
               room.active_users.remove(user)

        rooms_serializer = RoomSerializer(rooms, many=True)

    except Exception as e:
        return Response({'message':str(e), 'cause':str(e)})

    return Response({'message':'success', 'rooms':rooms_serializer.data})


@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def delete_room(request):
    try:
        room_id = request.data.get('room_id')
        room = Room.objects.get(id=int(room_id))
        room.delete()
        rooms = Room.objects.all()
        rooms_serializer = RoomSerializer(rooms, many=True)
    except Exception as e:
        return Response({'message':str(e), 'cause':str(e)})

    return Response({'message':'success', 'rooms':rooms_serializer.data })


@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def leave_room(request):
    try:
        user_id = request.data.get('user_id')
        room_id = request.data.get('room_id')
        user = User.objects.get(id=int(user_id))
        room = Room.objects.get(id=int(room_id))
        room.active_users.remove(user)
        rooms = Room.objects.all()
        rooms_serializer = RoomSerializer(rooms, many=True)
    except Exception as e:
        return Response({'message':str(e), 'cause':str(e)})

    return Response({'message':'success', 'rooms':rooms_serializer.data })


@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def exit_chat(request):
    try:
        user_id = request.data.get('user_id')
        user = User.objects.get(id=int(user_id))
        user.profile.in_chat = False
        user.profile.save()    
    except Exception as e:
        return Response({'message':str(e), 'cause':str(e)})

    return Response({'message':'success'})


@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def post_to_users(request):
    try:
        users = request.data.get('users').split(',')
        sender_id = request.data.get('sender_id')
        message = request.data.get('message')
        color = request.data.get('color')

        recipients = []
        recipient_ids = []
        channels = []

       
        for username in users:
            usr = User.objects.get(username=username)

            try:
                channel = UserChannel.objects.get(owner=usr)
            except Exception as e:
                channel = UserChannel.objects.create(name="Channel of {}".format(usr.username),
                                                     owner=usr)
            channels.append(channel)
            recipients.append(usr)
            recipient_ids.append(usr.id)
 
        user = User.objects.get(id=int(sender_id))
        user.profile.chat_color=color
        user.profile.save()
  
        message = Message.objects.create(body=message, color=color, sender=user)
        message.receivers.add(*recipients)         


        for channel in channels:
            channel.pending_messages.add(message)
            channel.save()

        id_lst = []    
        messages_list = Message.objects.filter(sender_id=int(sender_id), receivers__in=recipient_ids)
        rooms_list = Room.objects.all()
        messages_serializer = MessageSerializer(messages_list, many=True) 
        rooms_serializer = RoomSerializer(rooms_list, many=True)  
    except Exception as e:
        return Response({'message':str(e), 'cause':str(e)})

    
    return Response({'message':'success', 'messages':messages_serializer.data, 'rooms':rooms_serializer.data})



@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def post_to_room(request):
    try:
        rooms = request.data.get('rooms').split(',')
        sender_id = request.data.get('sender_id')
        color = request.data.get('color')
        active_room_id = request.data.get('active_room')
        message = request.data.get('message')
        user = User.objects.get(id=int(sender_id))
        user.profile.chat_color=color
        user.profile.save()


        for r in rooms:
            try:
                room = Room.objects.get(name=str(r))

            except Exception as e:

                room = Room.objects.create(creator=user, name=r)
            
            message = Message.objects.create(room=room, body=message, color=color, sender=user)

        messages_list = Message.objects.filter(room_id=int(active_room_id))
        rooms_list = Room.objects.all()
        messages_serializer = MessageSerializer(messages_list, many=True)
        rooms_serializer = RoomSerializer(rooms_list, many=True)
    except Exception as e:
        return Response({'message':str(e), 'cause':str(e)})

    return Response({'message':'success', 'messages':messages_serializer.data, 'rooms':rooms_serializer.data})


@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def save_chat_color(request):
    try:
        user_id = request.data.get('user_id')
        color = request.data.get('color')
        user = User.objects.get(id=int(user_id))
        user.profile.in_chat = True
        user.profile.chat_color = color
        user.profile.save()
    except Exception as e:
        log = Logger(log="DID NOT WORK - {}".format(e))
        log.save() 
        return Response({'message':str(e), 'cause':str(e)})

    return Response({'message':'success'})


@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def read_chat_color(request):
    try:
        user_id = request.data.get('user_id')
        user = User.objects.get(id=int(user_id))
        color = user.profile.chat_color

    except Exception as e:

        return Response({'message':str(e), 'cause':str(e)})

    return Response({'message':'success', 'color': color})


@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def enter_chat(request):
    try:
        user_id = request.data.get('user_id')
        user = User.objects.get(id=int(user_id))
        user.profile.in_chat = True
        user.profile.save()

        try:
            channel = UserChannel.objects.get(owner=user)
        except Exception as e:
            UserChannel.objects.create(name="Channel of {}".format(user.username),
                                       owner=user)
                                        
    except Exception as e:
        return Response({'message':str(e), 'cause':str(e)})
    
    return Response({'message':'success'})


@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def clean_pending(request):
    try:
        user_id = request.data.get('user_id')
        user = User.objects.get(id=int(user_id))
        channel = UserChannel.objects.get(owner=user)
        channel.pending_messages.clear()
    except Exception as e:

        return Response({'message':str(e), 'cause':str(e)})
    return Response({'message':'success'})


@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def send_message(request):
    return Response({'message':'success'})




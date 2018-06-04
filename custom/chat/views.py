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
from custom.forum.models import Emotion
from custom.forum.models import Topic
from custom.blog.models import Post
from custom.chat.signals import user_joined_chat
from custom.chat.signals import user_left_chat
from custom.chat.signals import chat_room_created
from custom.chat.signals import chat_room_terminated
from custom.chat.signals import user_joined_room
from custom.chat.signals import user_left_room
#from custom.chat.callbacks import user_joined_chat_handler
#from custom.chat.callbacks import user_left_chat_handler
#from custom.chat.callbacks import user_joined_room_handler
#from custom.chat.callbacks import user_left_room_handler
#from custom.chat.callbacks import chat_room_created_handler
#from custom.chat.callbacks import chat_room_terminated_handler

@csrf_exempt
@login_required
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
    except Exception as e:
            username = ''
            logout=False
            user_id = -1
            is_authenticated = False
            has_private = False

    return render(request, 'chat.html',{'home': 'chat.html',
                                        'user': request.user,
                                        'has_private': has_private,
                                        'username': username,
                                        'current_page': 'chat',
                                        'is_authenticated': is_authenticated,
                                        'logout': logout,
                                        'user_id': user_id})

def join_room(request):
    pass

def leave_room(request):
    pass

def send_message(request):
    pass




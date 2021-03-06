import cyrtranslit
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.signals import user_logged_out
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage

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

from custom.gui.views import chunks
from custom.gui.views import Page
from custom.blog.views import Post
from custom.forum.models import Topic
from custom.forum.models import Emotion
from custom.users.models import Relationship
from custom.users.models import Peer
from custom.users.signals import user_resend_activation
from custom.users.signals import user_send_reset_password_link
from custom.users.serializers import UserSerializer
from custom.users.callbacks import resend_activation_handler
from custom.users.callbacks import reset_password_link
from custom.users.models import UserSession
from custom.users.models import Profile
from custom.utils.models import Logger


class Login(APIView):
    def post(self, request):        
        username = request.data['username']
        password = request.data['password']
        
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:              
                login(request, user)                
                serializer = UserSerializer(user)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class Logout(APIView):
    queryset = User.objects.all()

    def get(self, request, format=None):
        # simply delete the token to force a login
        request.session.flush()
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def resend_activation_by_userid(request, user_id):
    username = request.data.get('username', '')

    try:
        user = User.objects.get(id=int(user_id))
    except ObjectDoesNotExist:
        return Response({"message": "failure - user not found",
                         "status": "failed",
                         "code": 400,
                         "falure_code": 1,
                         "user_id": -1},
                         status=400)
    except TypeError:
        return Response({"message": "failure - user id is not integer",
                         "status": "failed",
                         "code": 400,
                         "falure_code": 1,
                         "user_id": -1},
                         status=400)

    user_resend_activation.send(sender = user,
                                instance = user,
                                kwargs = None)

    return Response({"message": "success",
                     "status": "activation_resent",
                     "code": 200,
                     "user_id": 1,
                     "username": username},
                     status=200)


@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def resendactivationbyuser(request):
    username = request.data.get('username', '')

    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return Response({"message": "failure - user not found",
                         "status": "failed",
                         "code": 400,
                         "falure_code": 1,
                         "user_id": -1,
                         "username": username},
                         status=400)

    user_resend_activation.send(sender = user,
                                instance = user,
                                kwargs = None)

    return Response({"message": "success",
                     "status": "activation_resent",
                     "code": 200,
                     "user_id": 1,
                     "username": username},
                     status=200)

@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def resend_password_link(request):
    username = request.data.get('username', '')
    email = request.data.get('email', '')
    user = None

    try:
        user = User.objects.get(username=username, email=email)
    except ObjectDoesNotExist:
        return Response({"message": "failure - username not found",
                         "status": "registered",
                         "code": 400,
                         "falure_code": 1,
                         "user_id": -1,
                         "email": email,
                         "username": username},
                         status=400)
    try:
        user_send_reset_password_link.send(sender = user,
                                           instance = user,
                                           kwargs = None)
    except Exception as e:
        log = Logger(log="Could not send reset link {}".format(e))
        log.save()
        return Response({"message": "failure - username not found",
                         "status": "registered",
                         "code": 400,
                         "falure_code": 1,
                         "user_id": -1,
                         "email": email,
                         "username": username},
                         status=400)


    return Response({"message": "success",
                     "status": "registered",
                     "code": 200,
                     "user_id": 1,
                     "username": username},
                     status=200)

@csrf_exempt
@permission_classes([IsAuthenticated,])
@login_required(login_url='https://lovehate.io/')
def editprofile(request):
    redirect = 'mylh_avatar.html'
    username = request.POST.get('profile_username', '')
    user_id =  request.POST.get('profile_user_id', '')
    session_username = request.POST.get('session_username', '')
    first_name = request.POST.get('first_name', '')
    last_name = request.POST.get('last_name', '')
    email = request.POST.get('profile_email', '')
    bio = request.POST.get('bio', '')
    profile_image_path = None

    if request.method=='POST':
        profile_image_path = None
        avtr_file = request.FILES.get('avatar', None)

        if avtr_file:
            avatar = request.FILES['avatar']
            fs = FileSystemStorage()
            filename = fs.save(avatar.name, avatar)
            uploaded_file_url = fs.url(filename)
            profile_image_path = uploaded_file_url
        else:
            profile = request.user.profile  
            profile_image_path = profile.profile_image_path

    try:
        username_transliterated=cyrtranslit.to_latin(username, 'ru').lower()
        user = request.user
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email

        user.profile.username = username
        user.profile.first_name = first_name
        user.profile.bio = bio
        user.profile.email = email
        user.profile.username_transliterated = username_transliterated
        user.profile.profile_image_path = profile_image_path
        user.save()
        user.profile.save()
    except Exception as e:
        user = None
        log = Logger(log="Failed to save user {}".format(e))
        log.save()

    return HttpResponseRedirect('/mylh/')


@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def saveprofile(request):
    username = request.data.get('username', '')
    user_id =  request.data.get('user_id', '')
    session_username = request.data.get('session_username', '')
    first_name = request.data.get('first_name', '')
    last_name = request.data.get('last_name', '')
    email = request.data.get('email', '')
    bio = request.data.get('bio', '')
  
    log = Logger(log="FILE DICT {} {}".format(request.FILES, username))
    log.save()

   # if request.FILES['avatar']:
   #     myfile = request.FILES['avatar']
   #     fs = FileSystemStorage()
   #     filename = fs.save(myfile.name, myfile)
   #     uploaded_file_url = fs.url(filename)
        
    #    log = Logger(log="FILE URL {}".format(uploaded_file_url))
    #    log.save()


    try:
        username_transliterated=cyrtranslit.to_latin(username, 'ru').lower()
        existing_user = User.objects.get(username=username)
            
        if existing_user.id != int(user_id):
                return Response({"message": "failure - username used",
                                 "status": "registered",
                                 "code": 400,
                                 "falure_code": 1,
                                 "user_id": -1,
                                 "email": email,
                                 "username": username},
                                 status=400)

    except Exception as e:
        log = Logger(log="Failed to get existing {}".format(e))
        log.save()

    try:
        existing_user = User.objects.get(email=email)

        if existing_user.id != int(user_id):
                return Response({"message": "failure - username used",
                                 "status": "registered",
                                 "code": 400,
                                 "falure_code": 1,
                                 "user_id": -1,
                                 "email": email,
                                 "username": username},
                                 status=400)

    except Exception as e:
        log = Logger(log="Failed to get existing {}".format(e))
        log.save()


    try:
        user = User.objects.get(username=session_username)
    except Exception as e:
        log = Logger(log="Failed to read user {}".format(e))
        log.save()

        return Response({"message": "failure - user not found",
                         "status": "registered",
                         "code": 400,
                         "falure_code": 1,
                         "user_id": -1,
                         "email": email,
                         "username": username},
                         status=400)

    try:
        username_transliterated=cyrtranslit.to_latin(username, 'ru').lower()
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email

        user.profile.username = username
        user.profile.first_name = first_name
        user.profile.bio = bio
        user.profile.email = email
        user.profile.username_transliterated = username_transliterated
        user.save()
        user.profile.save()
    except Exception as e:
        log = Logger(log="Failed to save user {}".format(e))
        log.save()

        return Response({"message": "failure - failed to save",
                             "status": "registered",
                             "code": 400,
                             "falure_code": 1,
                             "user_id": -1,
                             "email": email,
                             "username": username},
                             status=400) 


    return Response({"message": "success",
                     "status": "updated",
                     "code": 200,
                     "user_id": user.id,
                     "username": username},
                     status=200)
   
 

@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def registernew(request):
    username = request.data.get('username', '')
    password = request.data.get('password', '')
    email = request.data.get('email', '')
    user = None

    try:
        username_transliterated=cyrtranslit.to_latin(username, 'ru').lower()
        profile = Profile.objects.get(username_transliterated=username_transliterated)
            
        return Response({"message": "failure - username used",
                         "status": "username_used",
                         "code": 400,
                         "falure_code": 1,
                         "user_id": -1,
                         "email": email,
                         "username": username},
                         status=400)

    except ObjectDoesNotExist as e:
        log = Logger(log="Search by username gave no results {}".format(e))
        log.save()


    try:
        user = User.objects.get(email=email)

        return Response({"message": "failure - email used",
                         "status": "email_used",
                         "code": 400,
                         "falure_code": 1,
                         "user_id": -1,
                         "email": email,
                         "username": username},
                         status=400)
    except ObjectDoesNotExist as e:
        log = Logger(log="Search by email gave no result {}".format(e))
        log.save()

    except Exception as e:
        log = Logger(log="EMAIL error {}".format(e))
        log.save()

        return Response({"message": "failure - email used",
                         "status": "email_used",
                          "code": 400,
                          "falure_code": 1,
                          "user_id": -1,
                          "email": email,
                          "username": username},
                          status=400)


    try:
        user = User.objects.create(username=username,
                                   email=email)
        user.set_password(password)
        user.save()

        if user:
            profile = Profile.objects.create(user=user,
                                             username=username,
                                             password=password,
                                             email=email,
                                             username_transliterated=cyrtranslit.to_latin(username, 'ru').lower(),
                                             is_activated=False,
                                             is_cleared=False,
                                             is_new=False)
            user_resend_activation.send(sender = user,
                                        instance = user,
                                        kwargs = None)
    except Exception as e:
        return Response({"message": "failure",
                         "status": "registered",
                         "code": 400,
                         "failure_code": 3,
                         "user_id": -1,
                         "email": email,
                         "username": username},
                         status=400)

    return Response({"message": "success",
                     "status": "registered",
                     "code": 200,
                     "user_id": 1,
                     "username": username},
                     status=200)


@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def addnewfriend(request):
    username = request.data.get('username', '')
    user_id = request.data.get('user_id', '')
    friends_delete = request.data.get('friends_delete', '')

    if len(friends_delete)> 0:
        for friend_id in friends_delete:
            try:
                f_id = int(friend_id)
                peer = Peer.objects.filter(acceptor_id=f_id, relation_id=1)
                peer.delete()
            except Exception as e:
                return Response({"message": "Failed to delete peer {}".format(e),
                                 "code":400,
                                 "message_error": str(e),
                                 "log_out": False,
                                 "status": "unauthenticated",
                                 "not_activated": False,
                                 "reason": "invalid user id"},
                                 status=400)
        return Response({"message": "success",
                         "status": "authenticated",
                         "code": 200,
                         "not_activated": False,
                         "user_id": user_id,
                         "username": username,
                         "log_out": True},
                         status=200)


    try:
        log = Logger(log="TRYING TO FIND HIM {}".format(username))
        log.save()
        username_transliterated=cyrtranslit.to_latin(username, 'ru').lower()
        profile = Profile.objects.get(username_transliterated=username_transliterated)
        acceptor = profile.user
    except Exception as e:
        log = Logger(log="FAILED TO FIND HIM {} = {}".format(username, e))
        log.save()
        return Response({"message": "User was not found",
                         "code":400,
                         "message_error": str(e),
                         "log_out": False,
                         "status": "unauthenticated",
                         "not_activated": False,
                         "reason": "invalid user id"},
                         status=400)

    try:
        initiator = User.objects.get(id=int(user_id))
        relation = Relationship.objects.get(id=1)
        not_found = False
    except Exception as e:
        log = Logger(log="FAILED TO FIND - HIM {} = {} =  {}".format(username, user_id, e))
        log.save()
        not_found = True
        return Response({"message": "User was not found",
                         "code":400,
                         "message_error": str(e),
                         "log_out": False,
                         "status": "unauthenticated",
                         "not_activated": False,
                         "reason": "invalid user id"},
                         status=400)

    try:
        peer = Peer.objects.get(acceptor=acceptor, initiator=initiator)
        peer.relation = relation
        peer.save()
    except ObjectDoesNotExist as e: 
        peer = Peer.objects.create(relation=relation, acceptor=acceptor, initiator=initiator, strength=1)
    except Exception as e:
        return Response({"message": "User was not found",
                         "code":400,
                         "message_error": str(e),
                         "log_out": False,
                         "status": "unauthenticated",
                         "not_activated": False,
                         "reason": "invalid user id"},
                         status=400)


    return Response({"message": "success",
                     "status": "authenticated",
                     "code": 200,
                     "not_activated": False,
                     "user_id": initiator.id,
                     "username": initiator.username,
                     "log_out": True},
                     status=200)



@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def addnewenemy(request):
    username = request.data.get('username', '')
    user_id = request.data.get('user_id', '')
    enemies_delete = request.data.get('enemies_delete', '')

    if len(enemies_delete)> 0:
        for enemy_id in enemies_delete:
            try:
                f_id = int(enemy_id)
                peer = Peer.objects.filter(acceptor_id=f_id, relation_id=3)
                peer.delete()
            except Exception as e:
                return Response({"message": "Failed to delete peer {}".format(e),
                                 "code":400,
                                 "message_error": str(e),
                                 "log_out": False,
                                 "status": "unauthenticated",
                                 "not_activated": False,
                                 "reason": "invalid user id"},
                                 status=400)
        return Response({"message": "success",
                         "status": "authenticated",
                         "code": 200,
                         "not_activated": False,
                         "user_id": user_id,
                         "username": username,
                         "log_out": True},
                         status=200)

    try:
        acceptor = User.objects.get(username=username)
    except Exception as e:
        return Response({"message": "User was not found",
                         "code":400,
                         "message_error": str(e),
                         "log_out": False,
                         "status": "unauthenticated",
                         "not_activated": False,
                         "reason": "invalid user id"},
                         status=400)


    try:
        initiator = User.objects.get(id=int(user_id))
        relation = Relationship.objects.get(id=3)
        not_found = False
    except Exception as e:
        not_found = True
        return Response({"message": "User was not found",
                         "code":400,
                         "message_error": str(e),
                         "log_out": False,
                         "status": "unauthenticated",
                         "not_activated": False,
                         "reason": "invalid user id"},
                         status=400)

    try:
        peer = Peer.objects.get(acceptor=acceptor, initiator=initiator)
        peer.relation = relation
        peer.save()
    except ObjectDoesNotExist as e:
        peer = Peer.objects.create(relation=relation, acceptor=acceptor, initiator=initiator, strength=1)


    return Response({"message": "success",
                     "status": "authenticated",
                     "code": 200,
                     "not_activated": False,
                     "user_id": initiator.id,
                     "username": initiator.username,
                     "log_out": True},
                     status=200)


def processfriends(request):
    username = request.POST.get('friend_username', '')

    try:
        has_private = request.user.profile.has_private
    except Exception as e:
        has_private = False

    try:
        user = User.objects.get(username=username)
        not_found = False
    except Exception as e:
        not_found = True  
    log = Logger(log="REQUESTED NEW FRIEND {}".format(username))
    log.save()

    return render(request, 'relationships.html', {'not_found': not_found, 
                                                  'has_private': has_private})



def processrivals(request):
    username = request.POST.get('rival_username', '')
    return render(request, 'relationships.html', {})


@permission_classes([IsAuthenticated,])
@login_required(login_url='https://lovehate.io/')
def user_relationships(request, user_id):
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
    try:
        friends = Peer.objects.filter(initiator=user_id, relation_id=1)
    except Exception as e:
        friends = []

    try:
        enemies = Peer.objects.filter(initiator=user_id, relation_id=3)
    except Exception as e:
        enemies = []
   
    add_enemies = []
    add_frields = []
 
    len_enemies = len(enemies)
    len_friends = len(friends)

    if len_friends > len_enemies:
        add_enemies_res = len_friends-len_enemies
        add_enemies = [''] * add_enemies_res
    elif len_enemies > len_friends:
        add_frields_res = len_enemies-len_friends
        add_frields = [''] * add_frields_res
 

    return render(request, 'relationships.html', {"user_id": user_id, 
                                                  "friends": friends, 
                                                  "enemies": enemies,
                                                  "user": request.user,
                                                  "username": username,
                                                  "add_frields": add_frields,
                                                  "add_enemies": add_enemies,
                                                  "has_private": has_private,
                                                  "is_authenticated": is_authenticated,
                                                  "current_page": "relationships",
                                                  "username": request.user.username,
                                                  "logout": False,
                                                  "user_id": ''})

def user_profile(request, user_id):


    try:
        profile = Profile.objects.get(user_id=int(user_id))
        posts = Post.objects.filter(author_id=int(user_id))
        loves = Emotion.objects.filter(user=profile.user, attitude_id=1)
        loved_titles = []
        friends = Peer.objects.filter(initiator_id=int(user_id), relation_id=1)
        enemies = Peer.objects.filter(initiator_id=int(user_id), relation_id=3)
        friended = Peer.objects.filter(acceptor_id=int(user_id), relation_id=1)
        enemied = Peer.objects.filter(acceptor_id=int(user_id), relation_id=3) 
        has_private = profile.has_private
        profile_image_path = profile.profile_image_path

        for love in loves:
             loved_titles.append(love.translit_subject)


        loved_titles = list(set(loved_titles))
        loved_topics = Topic.objects.filter(translit_name__in=loved_titles)


        mehs = Emotion.objects.filter(user=profile.user, attitude_id=2)
        meh_titles = []

        for meh in mehs:
             meh_titles.append(meh.translit_subject)         

        meh_titles = list(set(meh_titles))
        meh_topics = Topic.objects.filter(translit_name__in=meh_titles)

        hates = Emotion.objects.filter(user=profile.user, attitude_id=3)
        hate_titles = []
        for hate in hates:
             hate_titles.append(hate.translit_subject)
        hate_titles = list(set(hate_titles))
        hate_topics = Topic.objects.filter(translit_name__in=hate_titles)

    except Exception as e:
        
        return render(request, 'index.html',{'home':'index.html', 'has_private': False})

    if request.user:
        if request.user.is_authenticated:
            username = request.user.username
            is_authenticated = True
            has_private = request.user.profile.has_private
        else:
            username = ''
            is_authenticated = False
            has_private = False
    else:
        username = ''
        is_authenticated = False
        has_private = False
    redirect = 'user.html'

    if not profile_image_path:
        profile_image_path = '/media/default.png'

    return render(request, 'user.html', {'home':'user.html',
                                         'explored_user_id': user_id,
                                         'explored_username': profile.user.username,
                                         'username': profile.user.username,
                                         'is_activated': False,
                                         'has_private': has_private,
                                         'loves': loved_topics,
                                         'mehs': meh_topics,
                                         'hates': hate_topics,
                                         'friends': friends,
                                         'friended': friended,
                                         'enemied': enemied,
                                         'enemies': enemies,
                                         'bio': profile.bio,
                                         'posts': posts,
                                         'user': request.user,
                                         'profile_image_path': profile_image_path,
                                         'is_authenticated': is_authenticated,
                                         'current_page': 'user_profile',
                                         'username': request.user.username,
                                         'fullname': "{} {}".format(profile.user.first_name, profile.user.last_name),
                                         'resend_activation': False,
                                         'logout': False,
                                         'user_id': profile.user.id})


@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def reset(request, reset_key):
    page = request.GET.get('page')
    loves = None
    mehs = None
    hates = None

    try:
        loves = Emotion.objects.filter(attitude_id=1)
        mehs = Emotion.objects.filter(attitude_id=2)
        hates = Emotion.objects.filter(attitude_id=3)
        total_loves = len(loves)
        total_mehs = len(mehs)
        total_hates = len(hates)
    except Exception as e:
        pass

    loves_chunked = list(chunks(loves, 10))
    loves_chunked_length = len(loves_chunked)
    mehs_chunked = list(chunks(mehs, 10))
    mehs_chunked_length = len(mehs_chunked)
    hates_chunked = list(chunks(hates, 10))
    hates_chunked_length = len(hates_chunked)
    index = max([loves_chunked_length, mehs_chunked_length, hates_chunked_length])

    pages = []
    pages_loves = []
    pages_hates = []
    pages_mehs = []

    try:
        has_private = request.user.profile.has_private
    except Exception as e:
        has_private = False

    for i in range(0, index):
        try:
            pages_loves.append(loves_chunked[i])
        except Exception as e:
            pages_loves.append([])
        try:
            pages_mehs.append(mehs_chunked[i])
        except Exception as e:
            pages_mehs.append([])
        try:
            pages_hates.append(hates_chunked[i])
        except Exception as e:
            pages_hates.append([])

    for i in range(0, index):
        p = Page(pages_loves[i], pages_mehs[i], pages_hates[i])
        pages.append(p)

    paginator = Paginator(pages, 1) # Show 25 contacts per page

    paginator1 = Paginator(loves, 10)
    paginator2 = Paginator(mehs, 10)
    paginator3 = Paginator(hates, 10)


    try:
        meh_slice = paginator2.page(page)
    except PageNotAnInteger:
        meh_slice = paginator2.page(1)
    except EmptyPage:
        meh_slice = paginator2.page(paginator.num_pages)

    try:
        love_slice = paginator1.page(page)
    except PageNotAnInteger:
        love_slice = paginator1.page(1)
    except EmptyPage:
        love_slice = paginator1.page(paginator1.num_pages)

    try:
        hate_slice = paginator3.page(page)
    except PageNotAnInteger:
        hate_slice = paginator3.page(1)
    except EmptyPage:
        hate_slice = paginator3.page(paginator3.num_pages)


    try:
        pages_slice = paginator.page(page)
    except PageNotAnInteger:
        pages_slice = paginator.page(1)
    except EmptyPage:
        pages_slice = paginator.page(paginator4.num_pages)


    try:

        profile = Profile.objects.get(password_recovery_key=reset_key)
        redirect = 'index.html'
        login(request, profile.user, backend='custom.users.backends.LocalBackend') #the user is now logged in
      
        return render(request, redirect,{'home':'index.html',
                                         'user': profile.user,
                                         'pages': pages_slice,
                                         'loves': love_slice,
                                         'mehs': meh_slice,
                                         'has_private': has_private,
                                         'hates': hate_slice,
                                         'username': profile.user.username,
                                         'is_reset_required': True,
                                         'is_reset_possible': True,
                                         'logout': False,
                                         'user_id': profile.user.id})

    except Exception as e:
        log = Logger(log="Reset failed {} - {} ".format(e, reset_key))
        log.save()
        redirect = 'index.html'
        return render(request, redirect,{'home':'index.html',
                                         'user': '',
                                         'username': '',
                                         'pages': pages_slice,
                                         'loves': love_slice,
                                         'mehs': meh_slice,
                                         'hates': hate_slice,
                                         'has_private': has_private,
                                         'is_reset_required': True,
                                         'is_reset_possible': False,  
                                         'logout': False,
                                         'user_id': ''})

@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def activate(request, activation_key):
    page = request.GET.get('page')
    loves = None
    mehs = None
    hates = None

    try:
        has_private = request.user.profile.has_private
    except Exception as e:
        has_private = False

    try:
        loves = Emotion.objects.filter(attitude_id=1)
        mehs = Emotion.objects.filter(attitude_id=2)
        hates = Emotion.objects.filter(attitude_id=3)
        total_loves = len(loves)
        total_mehs = len(mehs)
        total_hates = len(hates)
    except Exception as e:
        pass

    loves_chunked = list(chunks(loves, 10))
    loves_chunked_length = len(loves_chunked)
    mehs_chunked = list(chunks(mehs, 10))
    mehs_chunked_length = len(mehs_chunked)
    hates_chunked = list(chunks(hates, 10))
    hates_chunked_length = len(hates_chunked)
    index = max([loves_chunked_length, mehs_chunked_length, hates_chunked_length])

    pages = []
    pages_loves = []
    pages_hates = []
    pages_mehs = []

    for i in range(0, index):
        try:
            pages_loves.append(loves_chunked[i])
        except Exception as e:
            pages_loves.append([])
        try:
            pages_mehs.append(mehs_chunked[i])
        except Exception as e:
            pages_mehs.append([])
        try:
            pages_hates.append(hates_chunked[i])
        except Exception as e:
            pages_hates.append([])

    for i in range(0, index):
        p = Page(pages_loves[i], pages_mehs[i], pages_hates[i])
        pages.append(p)

    paginator = Paginator(pages, 1) # Show 25 contacts per page

    paginator1 = Paginator(loves, 10)
    paginator2 = Paginator(mehs, 10)
    paginator3 = Paginator(hates, 10)


    try:
        meh_slice = paginator2.page(page)
    except PageNotAnInteger:
        meh_slice = paginator2.page(1)
    except EmptyPage:
        meh_slice = paginator2.page(paginator.num_pages)

    try:
        love_slice = paginator1.page(page)
    except PageNotAnInteger:
        love_slice = paginator1.page(1)
    except EmptyPage:
        love_slice = paginator1.page(paginator1.num_pages)

    try:
        hate_slice = paginator3.page(page)
    except PageNotAnInteger:
        hate_slice = paginator3.page(1)
    except EmptyPage:
        hate_slice = paginator3.page(paginator3.num_pages)


    try:
        pages_slice = paginator.page(page)
    except PageNotAnInteger:
        pages_slice = paginator.page(1)
    except EmptyPage:
        pages_slice = paginator.page(paginator4.num_pages)


    try:

        profile = Profile.objects.get(activation_key=activation_key)
        profile.is_new = False
        profile.is_cleared = True
        profile.is_activated = True
        profile.save()
        redirect = 'index.html'
        login(request, profile.user, backend='custom.users.backends.LocalBackend') #the user is now logged in
      
        return render(request, redirect,{'home':'index.html',
                                         'user': profile.user,
                                         'pages': pages_slice,
                                         'loves': love_slice,
                                         'mehs': meh_slice,
                                         'hates': hate_slice,
                                         'has_private': has_private,
                                         'username': profile.user.username,
                                         'is_activated': True,
                                         'resend_activation': False,
                                         'logout': False,
                                         'user_id': profile.user.id})

    except Exception as e:
        log = Logger(log="Activation failed {} - {} ".format(e, activation_key))
        log.save()
        redirect = 'index.html'
        return render(request, redirect,{'home':'index.html',
                                         'user': '',
                                         'username': '',
                                         'pages': pages_slice,
                                         'loves': love_slice,
                                         'mehs': meh_slice,
                                         'hates': hate_slice,
                                         'has_private': has_private,
                                         'resend_activation': True,
                                         'is_activated': False,
                                         'logout': False,
                                         'user_id': ''})

@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def recoverpassword(request):
    password = str(request.data.get('password', ''))
    user_id = request.data.get('user_id', '')

    try:
        user = User.objects.get(id=int(user_id))
        if user:
             authenticate(username=user.username, password=user.password)
        user.set_password(password)
        user.save()


    except Exception as e:
        return Response({"message": "User was not found",
                         "code":400,
                         "message_error": str(e),
                         "log_out": False,
                         "status": "unauthenticated",
                         "not_activated": False,
                         "reason": "invalid user id"},
                         status=400)

    return Response({"message": "success",
                     "status": "authenticated",
                     "code": 200,
                     "not_activated": False,
                     "user_id": user.id,
                     "username": user.username,
                     "log_out": True},
                     status=200)




@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def changepassword(request):
    oldpassword = str(request.data.get('oldpassword', ''))
    newpassword = str(request.data.get('newpassword', ''))
    user_id = request.data.get('user_id', '')

    try:
        usr = User.objects.get(id=int(user_id))
        user = authenticate(username=usr.username, password=oldpassword)
    except Exception as e:
        log = Logger(log="USER COULD NOT BE FOUND {}".format(e))
        log.save()

        try:
            user = User.objects.get(id=int(user_id))
            vaid = False
            
            if user.is_authenticated and user.is_superuser:
               user = authenticate(username=user.username, password=oldpassword)
               if user:
                   valid = True
        except Exception as e1:
            valid = False

        if not valid:
            return Response({"message": 'Старый пароль не найден!',
                             "code":400,
                             "message_error": str(e),
                             "log_out": False,
                             "status": "unauthenticated",
                             "not_activated": False,
                             "reason": "invalid old password"},
                             status=400)
    user.set_password(newpassword)
    user.save()

    return Response({"message": "success",
                     "status": "authenticated",
                     "code": 200,
                     "not_activated": False,
                     "user_id": user.id,
                     "username": user.username,
                     "log_out": True},
                     status=200)

@csrf_exempt
def authentic(request):
    logout(request)
    username = str(request.POST.get('username', ''))
    password = str(request.POST.get('password', ''))
    not_activated = False

    try:
        user = User.objects.get(username=username)
        password_valid = check_password(password, user.password)

        if password_valid:
            if not request.session.session_key:
                request.session.create()

        session = request.session.session_key
        if not password_valid:

            result = {"message": 'failure login for username {}'.format(username),
                      "code":400,
                      "log_out": False,
                      "status": "unauthenticated",
                      "not_activated": False,
                      "reason": "Invalid user"}
            js = json.dumps(result)
            return HttpResponseBadRequest(js)


        profile = user.profile
        login(request, user,  backend='custom.users.backends.LocalBackend')

        if not profile.is_activated:
            not_activated = True
            logout(request)

        result = {"message": 'success',
                  "code":200,
                  "user_id": user.id,
                  "username": username,
                  "not_activated": not_activated,
                  "log_out": False,
                  "status": "activated",
                  "reason": "User is logged in"}
        js = json.dumps(result)
        return HttpResponse(js)



    except Exception as e:
        log = Logger(log="Failed authenticating user - {}".format(e))
        log.save()

        result = {"message": 'failure {} for username {}'.format(e, username),
                  "code":400,
                  "log_out": False,
                  "status": "unauthenticated",
                  "not_activated": not_activated,
                  "reason": "Invalid user"}
        js = json.dumps(result)
        return HttpResponseBadRequest(js)



@api_view(['POST'])
@permission_classes([AllowAny,])
def auth(request):
    username = str(request.data.get('username', ''))
    password = str(request.data.get('password', ''))

    not_activated = False
    logout(request)

    try:
        user = User.objects.get(username=username)
        password_valid = check_password(password, user.password)
          
        if password_valid:
            if not request.session.session_key:
                request.session.create()

        session = request.session.session_key

        log = Logger(log="USERNAME {} PASSWORD {} VALID {} SESSION {}".format(username, password, password_valid, session))
        log.save()
        if not password_valid:
            return Response({"message": 'failure login for username {}'.format(username),
                             "code":400,
                             "log_out": False,
                             "status": "unauthenticated",
                             "not_activated": False,
                             "reason": "Invalid user"},
                             status=400)



        profile = user.profile

        if not profile.is_activated:
            not_activated = True
            logout(request)  
      #  else:
      #      login(request, user, backend='custom.users.backends.LocalBackend')
        else:
            log = Logger(log="CREATING USER SESSION {} {} {}".format(user, username, password))
            login(request, user,  backend='custom.users.backends.LocalBackend')

#        if not user.profile.is_activated:
#            not_activated = True
#            logout(request)
#
        return Response({"message": 'success',
                         "code":200,
                         "user_id": user.id,
                         "username": username,
                         "log_out": False,
                         "not_activated": not_activated,
                         "status": "activated",
                         "reason": "User is activated"},
                         status=200)

    except Exception as e:
        log = Logger(log="Failed authenticating - {}".format(e))
        log.save()

        return Response({"message": 'failure {} for username {}'.format(e, username),
                         "code":400,
                         "log_out": False,
                         "status": "unauthenticated",
                         "not_activated": not_activated,
                         "reason": "Invalid user"},
                         status=400)


def delete_user_sessions(user):
    user_sessions = UserSession.objects.filter(user = user)
    for user_session in user_sessions:
        user_session.session.delete()


def user_logged_in_handler(sender, request, user, **kwargs):
    UserSession.objects.get_or_create(
        user = user,
        session_id = request.session.session_key
    )

def user_logged_out_handler(sender, request, user, **kwargs):
    delete_user_sessions(user)


user_logged_out.connect(user_logged_out_handler)
user_logged_in.connect(user_logged_in_handler)
user_send_reset_password_link.connect(reset_password_link)
user_resend_activation.connect(resend_activation_handler)

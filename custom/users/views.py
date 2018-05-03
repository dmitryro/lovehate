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

from custom.forum.models import Topic
from custom.forum.models import Emotion
from custom.users.signals import user_resend_activation
from custom.users.serializers import UserSerializer
from custom.users.callbacks import resend_activation_handler
from custom.users.models import Profile
from custom.utils.models import Logger

class Logout(APIView):
    queryset = User.objects.all()

    def get(self, request, format=None):
        # simply delete the token to force a login
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
def registernew(request):
    username = request.data.get('username', '')
    password = request.data.get('password', '')
    email = request.data.get('email', '')
    user = None

    log = Logger(log='OUR CREDS {} {} {}'.format(username, password, email))
    log.save()

    try:
        user = User.objects.get(username=username)
        if not user:
            user = User.objects.get(email=email)
    except ObjectDoesNotExist:
        pass

    try:
        if user is not None:
            return Response({"message": "failure - username used",
                             "status": "registered",
                             "code": 400,
                             "falure_code": 1,
                             "user_id": -1,
                             "email": email,
                             "username": username},
                             status=400)
        user = User.objects.create(username=username,
                                   email=email,
                                   password=password)
        if user is not None:
            profile = Profile.objects.create(user=user,
                                             username=username,
                                             email=email,
                                             is_activated=False,
                                             is_cleared=False,
                                             is_new=False)
            user_resend_activation.send(sender = user,
                                        instance = user,
                                        kwargs = None)
    except Exception as e:
        log = Logger(log='READING USER FAILED {}'.format(e))
        log.save()
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

def user_profile(request, user_id):


    try:

        log = Logger(log="LET US TRY ================ {} {} ".format(user_id, request.user))
        log.save()

        profile = Profile.objects.get(user_id=int(user_id))

        loves = Emotion.objects.filter(user=profile.user, attitude_id=1)
        loved_titles = []

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

        return render(request, 'index.html',{'home':'index.html'})

    if request.user:
        if request.user.is_authenticated:
            username = request.user.username
            is_authenticated = True
        else:
            username = ''
            is_authenticated = False
    else:
        username = ''
        is_authenticated = False

    redirect = 'user.html'
    return render(request, 'user.html', {'home':'user.html',
                                         'explored_username': profile.user.username,
                                         'username': profile.user.username,
                                         'is_activated': False,
                                         'loves': loved_topics,
                                         'mehs': meh_topics,
                                         'hates': hate_topics,
                                         'bio': profile.bio,
                                         'user': request.user,
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
def activate(request, activation_key):
    try:

        profile = Profile.objects.get(activation_key=activation_key)
        profile.is_new = False
        profile.is_cleared = True
        profile.is_activated = True
        profile.save()
        redirect = 'index.html'
        login(request, profile.user, backend='django.contrib.auth.backends.ModelBackend') #the user is now logged in
      
        return render(request, redirect,{'home':'index.html',
                                         'user': profile.user,
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
                                         'resend_activation': True,
                                         'is_activated': False,
                                         'logout': False,
                                         'user_id': ''})

@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def auth(request):
    username = str(request.data.get('username', ''))
    password = str(request.data.get('password', ''))

   
    user = authenticate(username=username, password=password)

    if not user:
        try:
            user = User.objects.get(username=username, password=password)
        except Exception as e:
            pass

    if user and not user.profile.is_activated:
        return Response({"message": 'success',
                         "code":200,
                         "user_id": user.id,
                         "username": username,
                         "log_out": False,
                         "not_activated": True,
                         "status": "notactivated",
                         "reason": "User is not activated"},
                         status=200)
    if not user:
        return Response({"message": 'failure',
                         "code":400,
                         "log_out": False,
                         "status": "unauthenticated",
                         "not_activated": False,
                         "reason": "Invalid user"}, 
                         status=400)
    if user.is_active:
        request.session.set_expiry(1086400) #sets the exp. value of the session 
        login(request, user,  backend='django.contrib.auth.backends.ModelBackend') #the user is now logged in

    return Response({"message": "success",
                     "status": "authenticated",
                     "code": 200,
                     "not_activated": False,
                     "user_id": user.id,
                     "username": user.username,
                     "log_out": True},
                     status=200)

user_resend_activation.connect(resend_activation_handler)

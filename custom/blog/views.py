from pyshorteners import Shortener
from django.shortcuts import render
from django.contrib.auth import logout as log_out
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from custom.utils.models import Logger
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
from settings import settings

from custom.blog.models import Comment
from custom.blog.models import Post
from custom.forum.models import Attitude

@csrf_exempt
def newcomment(request, post_id):
    try:
        post = Post.objects.get(id=int(post_id))
    except Exception:
        post = None

    try:
        if post:
            comments = Comment.objects.filter(post=post)
        else:
            comments = []
    except Exception:
        comments = []
  
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

    return render(request, 'comment_new.html',{'home':'comment_new.html',
                                               'post': post,
                                               'comments': comments,
                                               'user': request.user,
                                               'username': username,
                                               'current_page': 'new_comment',
                                               'is_authenticated': is_authenticated,
                                               'logout': logout,
                                               'user_id': user_id})


@csrf_exempt
def blogcomments(request, post_id):
    comments = []
    try:
        post = Post.objects.get(id=int(post_id))
    except Exception:
        post = None

    try:
        if post:
            comments = Comment.objects.filter(post=post)
        else:
            comments = []
    except Exception:
        comments = []

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
    return render(request, 'comments.html',{'home':'comments.html',
                                             'post': post,
                                             'comments': comments,
                                             'user': request.user,
                                             'username': username,
                                             'current_page': 'blog_comments',
                                             'is_authenticated': is_authenticated,
                                             'logout': logout,
                                             'user_id': user_id})


@csrf_exempt
def blogpost(request, post_id):
    comments = []
    try:
        post = Post.objects.get(id=int(post_id))
    except Exception:
        post = None

    try:
        if post:
            comments = Comment.objects.filter(post=post)
        else:
            comments = []
    except Exception:
        comments = []

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

    return render(request, 'blog_post.html',{'home':'blog_post.html',
                                             'post': post,
                                             'comments': comments,
                                             'user': request.user,
                                             'username': username,
                                             'current_page': 'blog_post',
                                             'is_authenticated': is_authenticated,
                                             'logout': logout,
                                             'user_id': user_id})



@csrf_exempt
def newblog(request):
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

    return render(request, 'blog_new.html',{'home':'statistics.html',
                                            'user': request.user,
                                            'username': username,
                                            'current_page': 'new_blog',
                                            'is_authenticated': is_authenticated,
                                            'logout': logout,
                                            'user_id': user_id})


@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def addnewcomment(request):
    try:
        body = request.data.get('body', '')
        title = request.data.get('title', '')
        att = int(request.data.get('attitude', None))
        post_id = int(request.data.get('post_id', None))
        attitude = Attitude.objects.get(id=int(att))
        user_id = int(request.data.get('user_id', None))
        attitude = Attitude.objects.get(id=int(att))
        post = Post.objects.get(id=post_id)
       
        user = User.objects.get(id=user_id)
        Comment.objects.create(author=user, title=title, body=body, attitude=attitude, post=post)
    except Exception as e:
        log = Logger(log="Error in blogs - thi just did not work out - failed to create a new post {}".format(e))
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
def addnewblog(request):
    try:
        post = request.data.get('post', '')
        subject = request.data.get('subject', '')
        att = int(request.data.get('attitude', None))
        url = request.data.get('link', '')
        user_id = int(request.data.get('user_id', None))
        attitude = Attitude.objects.get(id=int(att))
        user_id = int(request.data.get('user_id', None))
        attitude = Attitude.objects.get(id=int(att))
        shortener = Shortener('Google', api_key=settings.GOOGLE_API_KEY)

        try:
            link = shortener.short(url)
        except Exception as e:
            link = None

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
        Post.objects.create(author=user, subject=subject, link=link, attitude=attitude, body=post, translit_subject=trans_subject)
    except Exception as e:
        log = Logger(log="Error in blogs - thi just did not work out - failed to create a new post {}".format(e))
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
def userblog(request, user_id):
    page = request.GET.get('page')

    try:
        posts = Post.objects.filter(author_id=int(user_id))

        paginator = Paginator(posts, 10)

        try:
            posts_slice = paginator.page(page)
        except PageNotAnInteger:
            posts_slice = paginator.page(1)
        except EmptyPage:
            posts_slice = paginator.page(paginator.num_pages)


        if request.user.is_authenticated:
            logout=True
            username = request.user.username
            user_id = request.user.id
            is_authenticated = True
        else:
            username = ''
            logout=False
            user_id = -1
            is_authenticated = False
    except Exception as e:
            username = ''
            logout=False
            user_id = -1
            is_authenticated = False
            posts_slice = []

    return render(request, 'user_blog.html',{'home':'user_blog.html',
                                         'user': request.user,
                                         'username': username,
                                         'posts': posts_slice,
                                         'current_page': 'user_blog',
                                         'is_authenticated': is_authenticated,
                                         'logout': logout,
                                         'user_id': user_id})


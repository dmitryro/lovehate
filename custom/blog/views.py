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
from ipware import get_client_ip

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
    ip, is_routable = get_client_ip(request)

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

    if request.user.is_authenticated:
        return render(request, 'comment_new.html',{'home':'comment_new.html',
                                                   'post': post,
                                                   'comments': comments,
                                                   'user': request.user,
                                                   'username': username,
                                                   'current_page': 'new_comment',
                                                   'is_authenticated': is_authenticated,
                                                   'logout': logout,
                                                   'user_id': user_id})
    else:
        return render(request, 'comment_new_unauth.html',{'home':'comment_new_unauth.html',
                                                   'post': post,
                                                   'comments': comments,
                                                   'user': request.user,
                                                   'username': username,
                                                   'current_page': 'new_comment',
                                                   'is_authenticated': is_authenticated,
                                                   'logout': logout,
                                                   'user_id': user_id})


@csrf_exempt
def editcomment(request, comment_id):
    ip, is_routable = get_client_ip(request)
    try:
         comment = Comment.objects.get(id=int(comment_id))
    except Exception as e:
         comment = None



    try:
        post = Post.objects.get(id=int(comment.post_id))
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

    return render(request, 'comment_edit.html',{'home':'comment_edit.html',
                                               'post': post,
                                               'comments': comments,
                                               'comment': comment,
                                               'user': request.user,
                                               'username': username,
                                               'current_page': 'edit_comment',
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
def editblog(request, post_id):
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
        post = Post.objects.get(id=int(post_id))
    except Exception as e:
        post = None
        username = ''
        logout=False
        user_id = -1
        is_authenticated = False

    return render(request, 'blog_edit.html',{'home':'blog_edit.html',
                                            'user': request.user,
                                            'username': username,
                                            'post': post,
                                            'current_page': 'edit_blog',
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

    if is_authenticated:
        redirect = 'blog_new.html'
    else:
        redirect = 'blog_new_unauth.html'
    return render(request, redirect,{'home':redirect,
                                            'user': request.user,
                                            'username': username,
                                            'current_page': 'new_blog',
                                            'is_authenticated': is_authenticated,
                                            'logout': logout,
                                            'user_id': user_id})


@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def addnewcommentunauth(request):
    try:
        body = request.data.get('body', '')
        title = request.data.get('title', '')
        att = int(request.data.get('attitude', None))
        post_id = int(request.data.get('post_id', None))
        username = request.data.get('comment_username', None)
        password = request.data.get('comment_password', None)
        ip, is_routable = get_client_ip(request)
        ip_address = str(ip)
        user = authenticate(username=username, password=password)
        if not user:
            return Response({"message": "failed to authenticated",
                             "status": "posted",
                             "code": 400,
                             "falure_code": 2}, status=400)


        login(request, user, backend='django.contrib.auth.backends.ModelBackend') #the user is now logged in
        attitude = Attitude.objects.get(id=int(att))
        log = Logger(log="BEFORE WE READ POST")
        log.save()
        Comment.objects.create(author=user, title=title, body=body, attitude=attitude, post_id=post_id, ip_address=ip_address)
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
def addnewcomment(request):
    try:
        body = request.data.get('body', '')
        title = request.data.get('title', '')
        att = int(request.data.get('attitude', None))
        post_id = int(request.data.get('post_id', None))
        cid = request.data.get('comment_id', None)
        ip, is_routable = get_client_ip(request)
        ip_address = str(ip)
        if cid:
            comment_id = int(cid)
        else:
            comment_id = 0

        attitude = Attitude.objects.get(id=int(att))
        user_id = int(request.data.get('user_id', None))
        attitude = Attitude.objects.get(id=int(att))
        post = Post.objects.get(id=post_id)
       
        user = User.objects.get(id=user_id)

        try:
            if comment_id is not 0:
                comment = Comment.objects.get(id=comment_id)

            if comment:
                if not body or len(body) is 0:
                    comment.delete()
                else:
                    comment.attitude = attitude
                    comment.body = body
                    comment.ip_address = ip_address
                    comment.save()
            else:
                Comment.objects.create(author=user, title=title, body=body, attitude=attitude, post=post, ip_address=ip_address)
        except Exception as e:
            Comment.objects.create(author=user, title=title, body=body, attitude=attitude, post=post, ip_address=ip_address)
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
def updatepost(request):
    try:
        ip, is_routable = get_client_ip(request)
        ip_address = str(ip)
        log = Logger(log='ip = {}'.format(ip))
        log.save()

        body = request.data.get('post', '')
        subject = request.data.get('subject', '')
        att = int(request.data.get('attitude', None))
        url = request.data.get('link', '')
        user_id = int(request.data.get('user_id', None))
        post_id = int(request.data.get('post_id', None))
        attitude = Attitude.objects.get(id=int(att))
 
        shortener = Shortener("Bitly", bitly_token=settings.BITLY_API_TOKEN)

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
        post = Post.objects.get(id=post_id)
        post.ip_address = ip_address
        post.subject = subject
        post.link = link
        post.attitude = attitude
        post.body = body
        post.translit_subject = trans_subject
        post.save()
    except Exception as e:
        log = Logger(log="SOME SHIT HAPPENED {}".format(e))
        log.save()
        return Response({"message": "failed - {}".format(e),
                         "status": "posted",
                         "code": 400,
                         "falure_code": 1}, status=400)

    return Response({"message": "success - post saved",
                     "status": "posted",
                     "code": 200,
                     "falure_code": 0}, status=200)


@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def addnewblogunauth(request):
    ip, is_routable = get_client_ip(request)
    ip_address = str(ip)

    try:
        post = request.data.get('post', '')
        subject = request.data.get('subject', '')
        att = int(request.data.get('attitude', None))
        url = request.data.get('link', '')
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        attitude = Attitude.objects.get(id=int(att))
        attitude = Attitude.objects.get(id=int(att))
        shortener = Shortener("Bitly", bitly_token=settings.BITLY_API_TOKEN)

        user = authenticate(username=username, password=password)
        if not user:
            return Response({"message": "failed to authenticated",
                             "status": "posted",
                             "code": 400,
                             "falure_code": 2}, status=400)


        login(request, user, backend='django.contrib.auth.backends.ModelBackend') #the user is now logged in



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

        Post.objects.create(author=user, subject=subject, link=link,
                            attitude=attitude, body=post,
                            translit_subject=trans_subject,
                            ip_address=ip_address)

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
    ip, is_routable = get_client_ip(request)
    ip_address = str(ip)

    try:
        post = request.data.get('post', '')
        subject = request.data.get('subject', '')
        att = int(request.data.get('attitude', None))
        url = request.data.get('link', '')
        user_id = int(request.data.get('user_id', None))
        attitude = Attitude.objects.get(id=int(att))
        user_id = int(request.data.get('user_id', None))
        attitude = Attitude.objects.get(id=int(att))
        shortener = Shortener("Bitly", bitly_token=settings.BITLY_API_TOKEN)

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
        Post.objects.create(author=user, subject=subject, link=link, 
                            attitude=attitude, body=post, 
                            translit_subject=trans_subject,
                            ip_address=ip_address)
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
        posts = Post.objects.filter(author_id=int(user_id)).order_by('-time_published')

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


from pyshorteners import Shortener
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from custom.utils.models import Logger
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.timezone import now
from django.utils import timezone
from datetime import datetime
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

from custom.forum.models import Message
from custom.blog.models import Comment
from custom.blog.models import Post
from custom.forum.models import Attitude
from custom.blog.signals import post_comment_added
from custom.blog.signals import post_comment_edited
from custom.blog.signals import post_comment_deleted
from custom.blog.callbacks import post_comment_added_handler
from custom.blog.callbacks import post_comment_edited_handler
from custom.blog.callbacks import post_comment_deleted_handler
from pytz import timezone as pytz

tz = pytz('Europe/Moscow')


@csrf_exempt
def newcomment(request, post_id):
    ip, is_routable = get_client_ip(request)

    try:
        has_private = request.user.profile.has_private
    except Exception as e:
        has_private = False


    try:
        post = Post.objects.get(id=int(post_id))
    #    post.time_last_commented = timezone.now().replace(tzinfo=tz)
    #    post.save()
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
                                                   'has_private': has_private,
                                                   'username': username,
                                                   'current_page': 'new_comment',
                                                   'is_authenticated': is_authenticated,
                                                   'logout': logout,
                                                   'user_id': user_id})
    else:
        return render(request, 'comment_new_unauth.html',
                      {'home':'comment_new_unauth.html',
                       'post': post,
                       'comments': comments,
                       'has_private': has_private,
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
        post_id = post.id
       # post.time_last_commented = timezone.now().replace(tzinfo=tz)
        comment.time_last_edited = timezone.now().replace(tzinfo=tz)
  #      post.time_last_edited = str(now)
        post.save()
        comment.save()
        if comment:
                post_comment_edited.send(sender = comment,
                                         instance = comment,
                                         kwargs = None)

    except Exception as e:
        log = Logger(log="Something went wrong {}".format(e))
        log.save()

        post_id = -1
        post = None

    try:
        comments = Comment.objects.filter(post=post)
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

    if is_authenticated:
        has_private = request.user.profile.has_private
    else:
        has_private = False

    return render(request, 'comment_edit.html',{'home':'comment_edit.html',
                                               'post': post,
                                               'post_id': post_id,
                                               'comments': comments,
                                               'has_private': has_private,
                                               'comment': comment,
                                               'user': request.user,
                                               'username': username,
                                               'current_page': 'edit_comment',
                                               'is_authenticated': is_authenticated,
                                               'logout': logout,
                                               'user_id': user_id})


@csrf_exempt
def blogcomments(request, post_id):
    page = request.GET.get('page')
    comments = []

    try:
        has_private = request.user.profile.has_private
    except Exception as e:
        has_private = False


    try:
        post = Post.objects.get(id=int(post_id))
    except Exception:
        post = None

    try:
        if post:
            comments = Comment.objects.filter(post=post)
        else:
            comments = []

        paginator = Paginator(comments, 500)

        try:
            comments_slice = paginator.page(page)
        except PageNotAnInteger:
            comments_slice = paginator.page(1)
        except EmptyPage:
            comments_slice = paginator.page(paginator.num_pages)
    except Exception:
        comments = []
        comments_slice = []


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

    return render(request, 'comments.html',
                  {'home':'comments.html',
                   'post': post,
                   'comments': comments_slice,
                   'user': request.user,
                   'has_private': has_private,
                   'username': username,
                   'current_page': 'blog_comments',
                   'is_authenticated': is_authenticated,
                   'logout': logout,
                   'user_id': user_id})


@csrf_exempt
def blogpost(request, post_id):
    comments = []

    try:
        has_private = False
        messages = Message.objects.filter(receiver_id=self.user.id, is_read=False)
        if len(messages) > 0:
            has_private = True
    except Exception as e:
        has_private = False


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

    return render(request, 'blog_post.html',
                  {'home':'blog_post.html',
                   'post': post,
                   'comments': comments,
                   'user': request.user,
                   'has_private': has_private,
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

    if is_authenticated:
        has_private = request.user.profile.has_private
    else:
        has_private = False

    return render(request, 'blog_edit.html',
                  {'home':'blog_edit.html',
                   'user': request.user,
                   'username': username,
                   'has_private': has_private,
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
        has_private = request.user.profile.has_private
        redirect = 'blog_new.html'
    else:
        has_private = False
        redirect = 'blog_new_unauth.html'
    return render(request, redirect,{'home':redirect,
                                     'user': request.user,
                                     'username': username,
                                     'current_page': 'new_blog',
                                     'has_private': has_private,
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
        post = Post.objects.get(id=post_id)
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

        login(request, user,  backend='custom.users.backends.LocalBackend') 
        #the user is now logged in

        if not user:
            return Response({"message": "failed to authenticated",
                             "status": "posted",
                             "code": 400,
                             "falure_code": 2}, status=400)


        attitude = Attitude.objects.get(id=int(att))
     
        comment = Comment.objects.create(author=user, title=title, 
                                         body=body, attitude=attitude, 
                                         post=post, ip_address=ip_address)
        if comment:
            post_comment_added.send(sender=comment,
                                    instance=comment,
                                    kwargs=None)

        post.time_last_commented = timezone.now().replace(tzinfo=tz)
        post.save()

    except Exception as e:
        log = Logger(log="Error in blogs- failed to create a new unauth post {}".format(e))
        log.save()
        return Response({"message": "failed - {}".format(e),
                         "status": "posted",
                         "code": 400,
                         "falure_code": 1}, status=400)

    return Response({"message": "success - username used",
                     "status": "posted",
                     "post_id": post_id,
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
        post_id = request.data.get('post_id', None)
        cid = request.data.get('comment_id', None)
        user_id = int(request.data.get('user_id', None))
 
        ip, is_routable = get_client_ip(request)
        ip_address = str(ip)
        if cid:
            comment_id = int(cid)
        else:
            comment_id = 0

        attitude = Attitude.objects.get(id=int(att))
        post = Post.objects.get(id=int(post_id))
        try:
            post.time_last_commented = timezone.now().replace(tzinfo=tz) 
            post.save()
        except Exception as e:
            log = Logger(log="Error updating post {} {}".format(e, post_id))
            log.save()
     
 
 
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
                comment = Comment.objects.create(author=user, title=title, 
                                                 body=body, attitude=attitude, 
                                                 post=post, ip_address=ip_address)
                if comment:
                    post_comment_added.send(sender=comment,
                                            instance=comment,
                                            kwargs=None)

        except Exception as e:
            comment = Comment.objects.create(author=user, title=title, 
                                             body=body, attitude=attitude, 
                                             post=post, ip_address=ip_address)
            if comment:
                post_comment_added.send(sender=comment,
                                        instance=comment,
                                        kwargs=None)


    except Exception as e:
        log = Logger(log="Error in blogs - this just did not work out - failed to create a new comment {}".format(e))
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
        url = request.data.get('link', None)
        url_two = request.data.get('link_two', None)
        url_three = request.data.get('link_three', None)
        url_four = request.data.get('link_four', '')
        user_id = int(request.data.get('user_id', None))
        post_id = int(request.data.get('post_id', None))
        attitude = Attitude.objects.get(id=int(att))
 
        try:
            if len(body) < 1:
                post = Post.objects.get(id=post_id)
                post.delete()
                return Response({"message": "success - post deleted",
                                 "status": "deleted",
                                 "code": 200,
                                 "falure_code": 0}, status=200)
        except Exception as e:
            log = Logger(log="Some error - {}".format(e))
            log.save()

        shortener = Shortener("Bitly", bitly_token=settings.BITLY_API_TOKEN)


        try:
            if url:
                link = shortener.short(url)
            else:
                link = None
        except Exception as e:
            link = None

        try:
            if url_two:
                link_two = shortener.short(url_two)
            else:
                link_two = None
        except Exception as e:
            link_two = None

        try:
            if url_three:
                link_three = shortener.short(url_three)
            else:
                link_three = None
        except Exception as e:
            link_three = None

        try:
            if url_four:
                link_four = shortener.short(url_four)
            else:
                link_four = None
        except Exception as e:
            link_four = None


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
        post.link_two = link_two
        post.link_three = link_three
        post.link_four = link_four
        post.attitude = attitude
        post.body = body
        post.time_last_edited = timezone.now().replace(tzinfo=tz)
        post.translit_subject = trans_subject
        post.save()
    except Exception as e:
        log = Logger(log='Failed saving the post {}'.format(e))
        log.save()
        return Response({"message": "failed - {}".format(e),
                         "status": "posted",
                         "code": 400,
                         "falure_code": 1}, status=400)

    return Response({"message": "success - post saved",
                     "status": "posted",
                     "code": 200,
                     "falure_code": 0}, status=200)


@csrf_exempt
def add_new_post(request):
    ip, is_routable = get_client_ip(request)
    ip_address = str(ip)

    try:
        post = request.POST.get('post', '')
        subject = request.POST.get('subject', '')
        att = int(request.POST.get('attitude', None))
        url = request.POST.get('link', '')
        url_two = request.POST.get('link_two', '')
        url_three = request.POST.get('link_three', '')
        url_four = request.POST.get('link_four', '')
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        attitude = Attitude.objects.get(id=int(att))
        attitude = Attitude.objects.get(id=int(att))
        shortener = Shortener("Bitly", bitly_token=settings.BITLY_API_TOKEN)

        user = authenticate(username=username, password=password)
        login(request, user, backend='custom.users.backends.LocalBackend') #the user is now logged in

        try:
            link = shortener.short(url)
        except Exception as e:
            link = None

        try:
            link_two = shortener.short(url_two)
        except Exception as e:
            link_two = None

        try:
            link_three = shortener.short(url_three)
        except Exception as e:
            link_three = None

        try:
            link_four = shortener.short(url_four)
        except Exception as e:
            link_four = None

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
                            link_two=link_two, link_three=link_three,
                            link_four=link_four,
                            attitude=attitude, body=post,
                            time_last_commented= timezone.now().replace(tzinfo=tz),
                            time_last_edited=timezone.now().replace(tzinfo=tz),
                            translit_subject=trans_subject,
                            ip_address=ip_address)
    except Exception as e:
        log = Logger(log="Error in blogs - thi just did not work out - failed to create a new post {}".format(e))
        log.save()

    return HttpResponseRedirect('/blog/')


@csrf_exempt
def add_new_post_unauth(request):
    ip, is_routable = get_client_ip(request)
    ip_address = str(ip)

    try:
        post = request.POST.get('blognew_post', '')
        
        subject = request.POST.get('blognew_subject', '')


        att = int(request.POST.get('blognew_attitude', 2))



        url = request.POST.get('blognew_link', '')
        url_two = request.POST.get('blognew_link_2', '')
        url_three = request.POST.get('blognew_link_3', '')
        url_four = request.POST.get('blognew_link_4', '')
        username = request.POST.get('blognew_username', None)
        password = request.POST.get('blognew_password', None)

        try:
            attitude = Attitude.objects.get(id=int(att))
        except Exception as e:
            attitude = Attitude.objects.get(id=2)


        shortener = Shortener("Bitly", bitly_token=settings.BITLY_API_TOKEN)

        user = authenticate(username=username, password=password)
        login(request, user,  backend='custom.users.backends.LocalBackend')

        try:
            link = shortener.short(url)
        except Exception as e:
            link = None

        try:
            link_two = shortener.short(url_two)
        except Exception as e:
            link_two = None

        try:
            link_three = shortener.short(url_three)
        except Exception as e:
            link_three = None

        try:
            link_four = shortener.short(url_four)
        except Exception as e:
            link_four = None

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
                            link_two=link_two, link_three=link_three,
                            link_four=link_four,
                            time_last_commented=timezone.now().replace(tzinfo=tz),
                            time_last_edited=timezone.now().replace(tzinfo=tz),
                            attitude=attitude, 
                            body=post,
                            translit_subject=trans_subject,
                            ip_address=ip_address)

    except Exception as e:
        log = Logger(log="Error adding new unauth post - failed to create a new post {}".format(e))
        log.save()

    return HttpResponseRedirect('/blog/')


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
        url_two = request.data.get('link_two', '')
        url_three = request.data.get('link_three', '')
        url_four = request.data.get('link_four', '')
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


        login(request, user)


        try:
            link = shortener.short(url)
        except Exception as e:
            link = None

        try:
            link_two = shortener.short(url_two)
        except Exception as e:
            link_two = None

        try:
            link_three = shortener.short(url_three)
        except Exception as e:
            link_three = None

        try:
            link_four = shortener.short(url_four)
        except Exception as e:
            link_four = None

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
                            link_two=link_two, link_three=link_three, 
                            link_four=link_four,
                            time_last_commented=timezone.now().replace(tzinfo=tz),
                            time_last_edited=timezone.now().replace(tzinfo=tz),
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
        url_two = request.data.get('link_two', '')
        url_three = request.data.get('link_three', '')
        url_four = request.data.get('link_four', '')

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
            link_two = shortener.short(url_two)
        except Exception as e:
            link_two = None

        try:
            link_three = shortener.short(url_three)
        except Exception as e:
            link_three = None

        try:
            link_four = shortener.short(url_four)
        except Exception as e:
            link_four = None

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
                            link_two=link_two, link_three=link_three,
                            link_four=link_four,
                            attitude=attitude, body=post,
                            time_last_commented=timezone.now().replace(tzinfo=tz),
                            time_last_edited=timezone.now().replace(tzinfo=tz),
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
def usercomments(request, user_id):
    page = request.GET.get('page')

    try:
        has_private = request.user.profile.has_private
    except Exception as e:
        has_private = False

    try:
        comments = Comment.objects.filter(author_id=int(user_id)).order_by('-time_published')
        explored_user_id = user_id
        explored = User.objects.get(id=int(user_id))
        explored_user_nickname = explored.username
        paginator = Paginator(comments, 10)

        try:
            comments_slice = paginator.page(page)
        except PageNotAnInteger:
            comments_slice = paginator.page(1)
        except EmptyPage:
            comments_slice = paginator.page(paginator.num_pages)


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
        explored_user_id = request.user.id
        explored_user_nickname = request.user.username
        username = ''
        logout=False
        user_id = -1
        is_authenticated = False
        comments_slice = []

    return render(request, 'user_comments.html',{'home':'user_comments.html',
                                                 'user': request.user,
                                                 'username': username,
                                                 'comments': comments_slice,
                                                 'has_private': has_private,
                                                 'explored_user_id': explored_user_id,
                                                 'explored_user_nickname': explored_user_nickname, 
                                                 'current_page': 'user_blog',
                                                 'is_authenticated': is_authenticated,
                                                 'logout': logout,
                                                 'user_id': user_id})



@csrf_exempt
def userblog(request, user_id):
    page = request.GET.get('page')

    try:
        has_private = request.user.profile.has_private
    except Exception as e:
        has_private = False


    try:
        posts = Post.objects.filter(author_id=int(user_id)).order_by('-time_last_commented')

        paginator = Paginator(posts, 100)

        try:
            posts_slice = paginator.page(page)
        except PageNotAnInteger:
            posts_slice = paginator.page(1)
        except EmptyPage:
            posts_slice = paginator.page(paginator.num_pages)


        if request.user.is_authenticated:
            logout = True
            username = request.user.username
            user_id = request.user.id
            is_authenticated = True
        else:
            username = ''
            logout = False
            user_id = -1
            is_authenticated = False
    except Exception as e:
            username = ''
            logout = False
            user_id = -1
            is_authenticated = False
            posts_slice = []

    return render(request, 'user_blog.html',
                  {'home':'user_blog.html',
                   'user': request.user,
                   'username': username,
                   'posts': posts_slice,
                   'has_private': has_private,
                   'current_page': 'user_blog',
                   'is_authenticated': is_authenticated,
                   'logout': logout,
                   'user_id': user_id})

post_comment_added.connect(post_comment_added_handler)
post_comment_edited.connect(post_comment_edited_handler)
post_comment_deleted.connect(post_comment_deleted_handler)

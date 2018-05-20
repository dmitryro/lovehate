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




class Page(object):
    def __init__(self, loves, mehs, hates):
        self.__loves = loves
        self.__mehs = mehs
        self.__hates = hates

    @property
    def loves(self):
        return self.__loves

    @property
    def hates(self):
        return self.__hates

    @property
    def mehs(self):
        return self.__mehs

    @mehs.setter
    def mehs(self, mehs):
        self.__mehs = mehs

    @loves.setter
    def loves(self, loves):
        self.__loves = loves

    @hates.setter
    def hates(self, hates):
        self.__hates = hates


def chunks(l, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i+n]


@csrf_exempt
def search(request):
    page = request.GET.get('page')
    query = request.GET.get('q','')
    cquery = query.capitalize()
    trans_query = ''
    query_transliterated=cyrtranslit.to_latin(query, 'ru').lower()

    try:
        
        posts = Post.objects.filter(Q(subject__icontains=query) |
                                    Q(body__icontains=query) |
                                    Q(subject__icontains=cquery) |
                                    Q(body__icontains=cquery) |
                                    Q(subject__icontains=query_transliterated) |
                                    Q(body__icontains=query_transliterated))
    except Exception as e:
        posts = []

    try:
        topics = Topic.objects.filter(Q(name__icontains=query) |
                                      Q(name__icontains=query_transliterated) |
                                      Q(name__icontains=cquery) |
                                      Q(translit_name__icontains=cquery) |
                                      Q(translit_name__icontains=query) |
                                      Q(translit_name__icontains=query_transliterated))
    except Exception as e:
        topics = []

    try:
        users = User.objects.filter(Q(username__icontains=query) |
                                    Q(username__icontains=query_transliterated) |
                                    Q(first_name__icontains=query) |
                                    Q(first_name__icontains=query_transliterated) |
                                    Q(last_name__icontains=query) |
                                    Q(last_name__icontains=query_transliterated))
    except Exception as e:
        users = []


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
       user_id = request.user.id
       user = User.objects.get(id=user_id)
    except Exception as e:
       user = request.user

    return render(request, 'search.html',{'search':'search.html',
                                         'user': user,
                                         'users': users,
                                         'topics': topics,
                                         'posts': posts,
                                         'has_private': has_private,
                                         'username': username,
                                         'is_authenticated': is_authenticated,
                                         'logout': logout,
                                         'user_id': user_id})


@csrf_exempt
def home(request):
    user_activity_objects = OnlineUserActivity.get_user_activities(timedelta(minutes=15))
    onliners = list(user for user in user_activity_objects)


    page = request.GET.get('page')
    loves = None
    mehs = None
    hates = None

    try:
        loves = Emotion.objects.filter(attitude_id=1).order_by('-time_published')
        mehs = Emotion.objects.filter(attitude_id=2).order_by('-time_published')
        hates = Emotion.objects.filter(attitude_id=3).order_by('-time_published')
        total_loves = len(loves)
        total_mehs = len(mehs)
        total_hates = len(hates)
    except Exception as e:
        pass

    loves_chunked = list(chunks(loves, 50))
    loves_chunked_length = len(loves_chunked)
    mehs_chunked = list(chunks(mehs, 50))
    mehs_chunked_length = len(mehs_chunked)
    hates_chunked = list(chunks(hates, 50))
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
        paginator1 = Paginator(loves, 50)
    except Exception as e:
        paginator1 = None

    try:
        if len(mehs)>=10:
            paginator2 = Paginator(mehs, 50)
        else:
            paginator2 = None
    except Exception as e:
        paginator2 = None

    try:
        paginator3 = Paginator(hates, 50)
    except Exception as e:
        patinator3 = None

    try:
        meh_slice = paginator2.page(page)
    except PageNotAnInteger:
        meh_slice = paginator2.page(1)
    except EmptyPage:
        meh_slice = paginator2.page(paginator2.num_pages)
        #else:
        #    meh_slice = []
    except Exception:
        meh_slice = []


    try:
        love_slice = paginator1.page(page)
    except PageNotAnInteger:
        love_slice = paginator1.page(1)
    except EmptyPage:
        love_slice = paginator1.page(paginator1.num_pages)
    except Exception:
        love_slice = []
 

    try:
        hate_slice = paginator3.page(page)
    except PageNotAnInteger:
        hate_slice = paginator3.page(1)
    except EmptyPage:
        hate_slice = paginator3.page(paginator3.num_pages)
    except Exception:
        hate_slice = []

  
    try:
        pages_slice = paginator.page(page)
    except PageNotAnInteger:
        pages_slice = paginator.page(1)
    except EmptyPage:
        pages_slice = paginator.page(paginator4.num_pages)
    except Exception:
        pages_slice = []
 

    try:
       user_id = request.user.id
       user = User.objects.get(id=user_id)
    except Exception as e:
       user = request.user

    return render(request, 'index.html',{'home':'index.html', 
                                         'user': user,
                                         'has_private': has_private,
                                         'pages': pages_slice,
                                         'onliners': onliners,
                                         'loves': love_slice,
                                         'mehs': meh_slice,
                                         'hates': hate_slice,
                                         'current_page': 'home',
                                         'username': username,
                                         'is_authenticated': is_authenticated,
                                         'logout': logout,
                                         'user_id': user_id})

@csrf_exempt
def private_contacts(request):
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

    return render(request, 'statistics.html',{'home':'contacts.html',
                                              'user': request.user,
                                              'has_private': has_private,
                                              'username': username,
                                              'current_page': 'private_contacts',
                                              'is_authenticated': is_authenticated,
                                              'logout': logout,
                                              'user_id': user_id})

@csrf_exempt
def private_settings(request):
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

    return render(request, 'statistics.html',{'home':'settings.html',
                                              'user': request.user,
                                              'has_private': has_private,
                                              'username': username,
                                              'current_page': 'private_settings',
                                              'is_authenticated': is_authenticated,
                                              'logout': logout,
                                              'user_id': user_id})



@csrf_exempt
def statistics(request):
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

    return render(request, 'statistics.html',{'home':'statistics.html',
                                              'user': request.user,
                                              'has_private': has_private,
                                              'username': username,
                                              'current_page': 'statistics',
                                              'is_authenticated': is_authenticated,
                                              'logout': logout,
                                              'user_id': user_id})

@csrf_exempt
def mylh(request):
    redirect = 'mylh_avatar.html'
    profile_image_path = None
    try:
        if request.user.is_authenticated:
            logout=True
            user_id = request.user.id
            username = request.user.username
            has_private = request.user.profile.has_private
            is_authenticated = True
            profile_image_path = request.user.profile.profile_image_path
        else:
            logout=False
            user_id = -1
            username = ''
            is_authenticated = False
            has_private = False
    except Exception as e:
            has_private = False
            username = ''
            logout=False
            user_id = -1
            is_authenticated = False

    return render(request, redirect,{'home':'mylh_avatar.html',
                                     'user': request.user,
                                     'username': username,
                                     'is_authenticated': is_authenticated,
                                     'current_page': 'mylh',
                                     'has_private': has_private,
                                     'profile_image_path': profile_image_path,
                                     'username': request.user.username,
                                     'logout': False,
                                     'user_id': ''})

@csrf_exempt
def mylh_avatar(request):
    redirect = 'mylh_avatar.html'
    profile_image_path = None
    try:
        if request.user.is_authenticated:
            logout=True
            user_id = request.user.id
            username = request.user.username
            has_private = request.user.profile.has_private
            is_authenticated = True
            profile_image_path = request.user.profile.profile_image_path
        else:
            logout=False
            user_id = -1
            username = ''
            is_authenticated = False
            has_private = False
    except Exception as e:
            has_private = False
            username = ''
            logout=False
            user_id = -1
            is_authenticated = False

    return render(request, redirect,{'home':'mylh_avatar.html',
                                     'user': request.user,
                                     'username': username,
                                     'is_authenticated': is_authenticated,
                                     'current_page': 'mylh_avatar',
                                     'has_private': has_private,
                                     'profile_image_path': profile_image_path,
                                     'username': request.user.username,
                                     'logout': False,
                                     'user_id': ''})


@csrf_exempt
def mylh_settings(request, user_id):
    redirect = 'mylh_settings.html'

    try:
        if request.user.is_authenticated:
            logout=True
            user_id = request.user.id
            username = request.user.username
            has_private = request.user.profile.has_private
            is_authenticated = True
        else:
            logout=False
            user_id = -1
            username = ''
            is_authenticated = False
            has_private = False
    except Exception as e:
            has_private = False
            username = ''
            logout=False
            user_id = -1
            is_authenticated = False

    return render(request, redirect,{'home':'mylh_settings.html',
                                     'user': request.user,
                                     'username': username,
                                     'is_authenticated': is_authenticated,
                                     'current_page': 'mylh_settings',
                                     'has_private': has_private,
                                     'username': request.user.username,
                                     'logout': False,
                                     'user_id': ''})

@csrf_exempt
def cleanmessages(request):
    todelete = request.POST.get('incoming_delete', [])
    
    for delete_id in todelete:
        try:
            message = Message.objects.get(id=delete_id)
            message.delete()
        except Exception as e:
            pass

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

    return render(request, 'incoming.html',{'home':'incoming.html',
                                            'user': request.user,
                                            'has_private': has_private,
                                            'username': username,
                                            'current_page': 'private',
                                            'is_authenticated': is_authenticated,
                                            'logout': logout,
                                            'user_id': user_id})


@csrf_exempt
def private(request, receiver_id=None):
    receiver_username = None

    if receiver_id:
        try:
            receiver = User.objects.get(id=int(receiver_id))
            receiver_username = receiver.username
        except Exception as e:
            pass
 
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

    return render(request, 'private.html',{'home':'private.html',
                                         'user': request.user,
                                         'username': username,
                                         'current_page': 'private',
                                         'has_private': has_private,
                                         'receiver_username': receiver_username,
                                         'is_authenticated': is_authenticated,
                                         'logout': logout,
                                         'user_id': user_id})


@csrf_exempt
def private_unauth(request, receiver_id=None):
    receiver_username = None

    if receiver_id:
        try:
            receiver = User.objects.get(id=int(receiver_id))
            receiver_username = receiver.username
        except Exception as e:
            pass

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

    return render(request, 'private_unauth.html',{'home':'private_unauth.html',
                                         'user': request.user,
                                         'username': username,
                                         'current_page': 'private',
                                         'has_private': has_private,
                                         'receiver_username': receiver_username,
                                         'is_authenticated': is_authenticated,
                                         'logout': logout,
                                         'user_id': user_id})

@csrf_exempt
def user_forum(request, user_id):
    page = request.GET.get('page')

    loves = None
    mehs = None
    hates = None

    try:
        loves = Emotion.objects.filter(attitude_id=1, user_id=int(user_id)).order_by('-time_published')
        mehs = Emotion.objects.filter(attitude_id=2, user_id=int(user_id)).order_by('-time_published')
        hates = Emotion.objects.filter(attitude_id=3, user_id=int(user_id)).order_by('-time_published')
        total_loves = len(loves)
        total_mehs = len(mehs)
        total_hates = len(hates)
    except Exception as e:
        pass

    loves_chunked = list(chunks(loves, 50))
    loves_chunked_length = len(loves_chunked)
    mehs_chunked = list(chunks(mehs, 50))
    mehs_chunked_length = len(mehs_chunked)
    hates_chunked = list(chunks(hates, 50))
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

    paginator1 = Paginator(loves, 50)
    paginator2 = Paginator(mehs, 50)
    paginator3 = Paginator(hates, 50)

    try:
        meh_slice = paginator2.page(page)
    except PageNotAnInteger:
        meh_slice = paginator2.page(1)
    except EmptyPage:
        meh_slice = paginator2.page(paginator2.num_pages)
    except Exception:
        meh_slice = []

    try:
        love_slice = paginator1.page(page)
    except PageNotAnInteger:
        love_slice = paginator1.page(1)
    except EmptyPage:
        love_slice = paginator1.page(paginator1.num_pages)
    except Exception:
        love_slice = []


    try:
        hate_slice = paginator3.page(page)
    except PageNotAnInteger:
        hate_slice = paginator3.page(1)
    except EmptyPage:
        hate_slice = paginator3.page(paginator3.num_pages)
    except Exception:
        hate_slice = []



    try:
        pages_slice = paginator.page(page)
    except PageNotAnInteger:
        pages_slice = paginator.page(1)
    except EmptyPage:
        pages_slice = paginator.page(paginator4.num_pages)

    return render(request, 'forum.html',{'home':'forum.html',
                                         'user': request.user,
                                         'pages': pages_slice,
                                         'loves': love_slice,
                                         'mehs': meh_slice,
                                         'hates': hate_slice,
                                         'current_page': 'forum',
                                         'has_private': has_private,
                                         'username': username,
                                         'is_authenticated': is_authenticated,
                                         'logout': logout,
                                         'user_id': user_id})
@csrf_exempt
def forum(request):
    page = request.GET.get('page')
    loves = None
    mehs = None
    hates = None

    user_activity_objects = OnlineUserActivity.get_user_activities(timedelta(minutes=15))
    onliners = list(user for user in user_activity_objects)


    try:
        loves = Emotion.objects.filter(attitude_id=1).order_by('-time_published')
        mehs = Emotion.objects.filter(attitude_id=2).order_by('-time_published')
        hates = Emotion.objects.filter(attitude_id=3).order_by('-time_published')
        total_loves = len(loves)
        total_mehs = len(mehs)
        total_hates = len(hates)
    except Exception as e:
        pass

    loves_chunked = list(chunks(loves, 50))
    loves_chunked_length = len(loves_chunked)
    mehs_chunked = list(chunks(mehs, 50))
    mehs_chunked_length = len(mehs_chunked)
    hates_chunked = list(chunks(hates, 50))
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

    paginator1 = Paginator(loves, 50)
    paginator2 = Paginator(mehs, 50)
    paginator3 = Paginator(hates, 50)

    try:
        meh_slice = paginator2.page(page)
    except PageNotAnInteger:
        meh_slice = paginator2.page(1)
    except EmptyPage:
        meh_slice = paginator2.page(paginator2.num_pages)
    except Exception:
        meh_slice = []

    try:
        love_slice = paginator1.page(page)
    except PageNotAnInteger:
        love_slice = paginator1.page(1)
    except EmptyPage:
        love_slice = paginator1.page(paginator1.num_pages)
    except Exception:
        love_slice = []
 

    try:
        hate_slice = paginator3.page(page)
    except PageNotAnInteger:
        hate_slice = paginator3.page(1)
    except EmptyPage:
        hate_slice = paginator3.page(paginator3.num_pages)
    except Exception:
        hate_slice = []


  
    try:
        pages_slice = paginator.page(page)
    except PageNotAnInteger:
        pages_slice = paginator.page(1)
    except EmptyPage:
        pages_slice = paginator.page(paginator4.num_pages)
 
    return render(request, 'forum.html',{'home':'forum.html', 
                                         'user': request.user,
                                         'pages': pages_slice,
                                         'loves': love_slice,
                                         'mehs': meh_slice,
                                         'onliners': onliners,
                                         'hates': hate_slice,
                                         'current_page': 'forum',
                                         'has_private': has_private,
                                         'username': username,
                                         'is_authenticated': is_authenticated,
                                         'logout': logout,
                                         'user_id': user_id})


def autneticate_user(username, password):
    user = authenticate(username=username, password=password)
    request.session.set_expiry(1086400) #sets the exp. value of the session
    login(request, user, backend='custom.users.backends.LocalBackend') #the user is now logged in
    return request   


@require_http_methods(["GET", "POST"]) 
@csrf_exempt
def simple_signin(request):

    user_activity_objects = OnlineUserActivity.get_user_activities(timedelta(minutes=15))
    onliners = (user for user in user_activity_objects)
 
    try:
        loves = Emotion.objects.filter(attitude_id=1)
        mehs = Emotion.objects.filter(attitude_id=2)
        hates = Emotion.objects.filter(attitude_id=3)

        username = request.POST.get('uname')
        password = request.POST.get('psw')
        user = authenticate(username=username, password=password)
        login(request, user, backend='custom.users.backends.LocalBackend') #the user is now logged in
 

        if request.user.is_authenticated:
            logout=True
            user_id = user.id
            username = user.username
            is_authenticated = True
            has_private = request.user.profile.has_private
        else:
            logout=False
            user_id = -1
            username = ''
            is_authenticated = False
            has_private = False
    except Exception as e:
            log = Logger(log="SOMETHING WENT WRONG {}".format(e))
            log.save()
            username = ''
            logout = False
            user_id = -1
            user = request.user
            is_authenticated = False
            has_private = False

    return render(request, 'index.html',{'home':'index.html',
                                         'user': user,
                                         'loves': loves,
                                         'mehs': mehs,
                                         'hates': hates,
                                         'has_private': has_private,
                                         'username': user.username,
                                         'is_authenticated': is_authenticated,
                                         'logout': logout,
                                         'user_id': user.id})

#    return render_to_response(request, 'index.html',{'home':'index.html',
#                                                     'user': user,
#                                                     'has_private': has_private,
#                                                     'loves': loves,
#                                                     'mehs': mehs,
#                                                     'hates': hates,
#                                                     'username': user.username,
#                                                     'is_authenticated': is_authenticated,
#                                                     'logout': logout,
#                                                     'user_id': user.id})


@csrf_exempt
def blog(request):
    page = request.GET.get('page')

    user_activity_objects = OnlineUserActivity.get_user_activities(timedelta(minutes=15))
    onliners = (user for user in user_activity_objects)

    try:
        posts = Post.objects.all().order_by('-time_last_commented')

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
            has_private = request.user.profile.has_private
        else:
            username = ''
            logout=False
            user_id = -1
            is_authenticated = False
            has_private = False
    except Exception as e:
            has_private = False
            username = ''
            logout=False
            user_id = -1
            is_authenticated = False
            posts_slice = []

    return render(request, 'blog.html',{'home':'blog.html',
                                         'user': request.user,
                                         'username': username,
                                         'has_private': has_private,
                                         'posts': posts_slice, 
                                         'current_page': 'blog',
                                         'is_authenticated': is_authenticated,
                                         'logout': logout,
                                         'user_id': user_id})


@csrf_exempt
def register(request):

    try:

        if request.user.is_authenticated:
            logout=True
            username = request.user.username
            user_id = request.user.id
            is_authenticated = True
            has_private = request.user.profile.has_private
            redirect = 'index.html'
        else:
            username = ''
            logout=False
            user_id = -1
            is_authenticated = False
            has_private = False
            redirect = 'register.html'
    except Exception as e:
            rediredt = 'register.html'
            username = ''
            logout=False
            user_id = -1
            is_authenticated = False
            has_private = False

    return render(request, redirect,{'home':'index.html',
                                         'user': request.user,
                                         'username': username,
                                         'has_private': has_private,
                                         'current_page': 'register',
                                         'is_authenticated': is_authenticated,
                                         'logout': logout,
                                         'user_id': user_id})



@csrf_exempt
@login_required
def logout(request):
    log_out(request)
    return HttpResponseRedirect('/')

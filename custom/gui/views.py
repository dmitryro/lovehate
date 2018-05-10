from django.shortcuts import render
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
def home(request):
    page = request.GET.get('page')
    loves = None
    mehs = None
    hates = None

    try:
        loves = Emotion.objects.filter(attitude_id=1).order_by('-time_published').order_by('-time_last_edited')
        mehs = Emotion.objects.filter(attitude_id=2).order_by('-time_published').order_by('-time_last_edited')
        hates = Emotion.objects.filter(attitude_id=3).order_by('-time_published').order_by('-time_last_edited')
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
 

    log = Logger(log="PAGES SLICE IS {} and NUMBER OF PAGES {}".format(pages_slice, paginator.num_pages))
    log.save()

    return render(request, 'index.html',{'home':'index.html', 
                                         'user': request.user,
                                         'pages': pages_slice,
                                         'loves': love_slice,
                                         'mehs': meh_slice,
                                         'hates': hate_slice,
                                         'current_page': 'home',
                                         'username': username,
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
    return render(request, 'statistics.html',{'home':'statistics.html',
                                              'user': request.user,
                                              'username': username,
                                              'current_page': 'statistics',
                                              'is_authenticated': is_authenticated,
                                              'logout': logout,
                                              'user_id': user_id})


def mylh(request):
    redirect = 'mylh.html'

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

    return render(request, redirect,{'home':'mylh.html',
                                     'user': request.user,
                                     'username': username,
                                     'is_authenticated': is_authenticated,
                                     'current_page': 'mylh',
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

    return render(request, 'incoming.html',{'home':'incoming.html',
                                            'user': request.user,
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

    return render(request, 'private.html',{'home':'private.html',
                                         'user': request.user,
                                         'username': username,
                                         'current_page': 'private',
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

    return render(request, 'private_unauth.html',{'home':'private_unauth.html',
                                         'user': request.user,
                                         'username': username,
                                         'current_page': 'private',
                                         'receiver_username': receiver_username,
                                         'is_authenticated': is_authenticated,
                                         'logout': logout,
                                         'user_id': user_id})

@csrf_exempt
def forum(request):
    page = request.GET.get('page')
    loves = None
    mehs = None
    hates = None

    try:
        loves = Emotion.objects.filter(attitude_id=1).order_by('-time_published').order_by('-time_last_edited')
        mehs = Emotion.objects.filter(attitude_id=2).order_by('-time_published').order_by('-time_last_edited')    
        hates = Emotion.objects.filter(attitude_id=3).order_by('-time_published').order_by('-time_last_edited')
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
                                         'username': username,
                                         'is_authenticated': is_authenticated,
                                         'logout': logout,
                                         'user_id': user_id})


def autneticate_user(username, password):
    user = authenticate(username=username, password=password)
    request.session.set_expiry(1086400) #sets the exp. value of the session
    login(request, user, backend='django.contrib.auth.backends.ModelBackend') #the user is now logged in
    return request   


@require_http_methods(["GET", "POST"]) 
@csrf_exempt
def simple_signin(request):
 
    try:
        loves = Emotion.objects.filter(attitude_id=1)
        mehs = Emotion.objects.filter(attitude_id=2)
        hates = Emotion.objects.filter(attitude_id=3)

        username = request.POST.get('uname')
        password = request.POST.get('psw')
        user = authenticate(username=username, password=password)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend') #the user is now logged in
 

        if request.user.is_authenticated:
            logout=True
            user_id = user.id
            username = user.username
            is_authenticated = True
        else:
            logout=False
            user_id = -1
            username = ''
            is_authenticated = False
    except Exception as e:
            log = Logger(log="SOMETHING WENT WRONG {}".format(e))
            log.save()
            username = ''
            logout = False
            user_id = -1
            user = request.user
            is_authenticated = False

    return render(request, 'index.html',{'home':'index.html',
                                         'user': user,
                                         'loves': loves,
                                         'mehs': mehs,
                                         'hates': hates,
                                         'username': user.username,
                                         'is_authenticated': is_authenticated,
                                         'logout': logout,
                                         'user_id': user.id})

@csrf_exempt
def blog(request):
    page = request.GET.get('page')

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

    return render(request, 'blog.html',{'home':'blog.html',
                                         'user': request.user,
                                         'username': username,
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
            redirect = 'index.html'
        else:
            username = ''
            logout=False
            user_id = -1
            is_authenticated = False
            redirect = 'register.html'
    except Exception as e:
            rediredt = 'register.html'
            username = ''
            logout=False
            user_id = -1
            is_authenticated = False

    return render(request, redirect,{'home':'index.html',
                                         'user': request.user,
                                         'username': username,
                                         'current_page': 'register',
                                         'is_authenticated': is_authenticated,
                                         'logout': logout,
                                         'user_id': user_id})



@csrf_exempt
def logout(request):
    log_out(request)
    return HttpResponseRedirect('/')

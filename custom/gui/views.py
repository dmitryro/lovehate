from django.shortcuts import render
from django.contrib.auth import logout as log_out
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from custom.utils.models import Logger
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from custom.forum.models import Emotion

@csrf_exempt
def home(request):
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
        log = Logger(log = 'LOVES {} MEHS {} HATES {}'.format(total_loves, total_mehs, total_hates))
        log.save()
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
 
    return render(request, 'index.html',{'home':'index.html', 
                                         'user': request.user,
                                         'loves': loves,
                                         'mehs': mehs,
                                         'hates': hates,
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
def private(request):

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
                                         'is_authenticated': is_authenticated,
                                         'logout': logout,
                                         'user_id': user_id})


@csrf_exempt
def forum(request):

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

    return render(request, 'forum.html',{'home':'forum.html',
                                         'user': request.user,
                                         'username': username,
                                         'current_page': 'forum',
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
                                         'username': user.username,
                                         'is_authenticated': is_authenticated,
                                         'logout': logout,
                                         'user_id': user.id})


@csrf_exempt
def blog(request):
    try:
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

    return render(request, 'blog.html',{'home':'blog.html',
                                         'user': request.user,
                                         'username': username,
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

    if request.user.is_authenticated:
        logout=True
        try:
           user_id = request.user.id
           username = request.user.username
           first_name = request.user.first_name
           last_name = request.user.last_name
           profile_image_path = ''
        except Exception as e:
           user_id = -1
           username = ''
           first_name = ''
           last_name = ''
           profile_image_path = ''

    else:
        user_id = -1
        logout=False
        username = ''
        first_name = ''
        last_name = ''
        profile_image_path = ''

    return HttpResponseRedirect('/')

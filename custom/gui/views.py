from django.shortcuts import render
from django.contrib.auth import logout as log_out
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from custom.utils.models import Logger
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods

@csrf_exempt
def home(request):
    
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
                                         'is_authenticated': is_authenticated,
                                         'logout': logout,
                                         'user_id': user_id})


@csrf_exempt
def mylh(request):

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

    return render(request, 'mylh.html',{'home':'mylh.html',
                                         'user': request.user,
                                         'username': username,
                                         'is_authenticated': is_authenticated,
                                         'logout': logout,
                                         'user_id': user_id})


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

    return render(request, 'index.html',{'home':'index.html',
                                         'user': request.user,
                                         'username': username,
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

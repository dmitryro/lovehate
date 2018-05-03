"""lovehate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import grappelli
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls.i18n import i18n_patterns
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers, serializers, viewsets
from rest_framework import generics
from rest_framework import viewsets, routers
from rest_framework.authtoken import views as drf_views
from rest_auth.views import LoginView

from custom.gui.views import home
from custom.gui.views import blog
from custom.gui.views import register
from custom.gui.views import logout
from custom.gui.views import forum
from custom.gui.views import mylh
from custom.gui.views import private
from custom.gui.views import statistics
from custom.gui.views import simple_signin
from custom.users.views import UserList
from custom.users.views import UserDetail
from custom.users.views import auth
from custom.users.views import activate
from custom.users.views import user_profile
from custom.users.views import registernew
from custom.users.views import resendactivationbyuser
from custom.users.views import Logout
from custom.forum.views import forum_new
from custom.forum.views import EmotionDetail
from custom.forum.views import EmotionList
from custom.forum.views import AttitudeDetail
from custom.forum.views import AttitudeList
from custom.forum.views import newemotion
from custom.forum.views import topics
from custom.forum.views import newmessage
from django.contrib import admin

urlpatterns = [
    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('', home),
    path('add/', forum_new),
    path('admin/', admin.site.urls),
    path('authenticate/', csrf_exempt(auth)),
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
    path('user/<int:user_id>/', user_profile),
    path('topics/<int:topic_id>/', topics),
    path('activate/<activation_key>/', activate),
    path('api-auth/', include('rest_framework.urls')),      
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('emotions/', EmotionList.as_view()),
    path('attitudes/', AttitudeList.as_view()),
    path('addnewemotion/', csrf_exempt(newemotion)),
    path('emotions/<int:pk>/', EmotionDetail.as_view()),
    path('attitudes/<int:pk>/', AttitudeDetail.as_view()),
    path('accounts/', include('allauth.urls')),
    path('api-token-auth/', csrf_exempt(obtain_jwt_token)),
    path('refresh-token/', csrf_exempt(refresh_jwt_token)),
    path('verify-token/', csrf_exempt(verify_jwt_token)),
    path('logout/', Logout.as_view()),
    path('signin/', simple_signin),
    path('signout/', logout),
    path('statistics/', statistics),
    path('register/', register),
    path('private/', private),
    path('forum/', forum),
    path('mylh/', mylh),
    path('blog/', blog),
    path('blogs/', blog),
    path('registernew/', registernew),
    path('newmessage/', newmessage),
    path('resendactivationbyuser/', resendactivationbyuser),
]

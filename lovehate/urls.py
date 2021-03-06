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
from custom.gui.views import search
from custom.gui.views import logout
from custom.gui.views import forum
from custom.gui.views import user_forum
from custom.gui.views import mylh
from custom.gui.views import mylh_avatar
from custom.gui.views import mylh_settings
from custom.gui.views import private
from custom.gui.views import private_unauth
from custom.gui.views import private_settings
from custom.gui.views import private_contacts
from custom.gui.views import cleanmessages
from custom.gui.views import statistics
from custom.gui.views import simple_signin
from custom.gui.views import signin
from custom.users.views import UserList
from custom.users.views import UserDetail
from custom.users.views import auth
from custom.users.views import authentic
from custom.users.views import activate
from custom.users.views import user_profile
from custom.users.views import registernew
from custom.users.views import resendactivationbyuser
from custom.users.views import resend_activation_by_userid
from custom.users.views import Logout
from custom.users.views import Login
from custom.users.views import changepassword
from custom.users.views import addnewfriend
from custom.users.views import addnewenemy
from custom.forum.views import forum_new
from custom.forum.views import forum_add
from custom.forum.views import forum_edit
from custom.forum.views import EmotionDetail
from custom.forum.views import EmotionList
from custom.forum.views import AttitudeDetail
from custom.forum.views import AttitudeList
from custom.forum.views import newemotion
from custom.forum.views import editemotion
from custom.forum.views import newemotion_unauth
from custom.forum.views import topics
from custom.forum.views import newmessage
from custom.forum.views import newmessage_unauth
from custom.forum.views import outgoing_messages
from custom.forum.views import incoming_messages
from custom.forum.views import incoming_user_messages
from custom.forum.views import answer_private
from custom.forum.views import answer_all_private
from custom.forum.views import read_private
from custom.forum.views import read_all_private
from custom.blog.views import addnewblog
from custom.blog.views import addnewblogunauth
from custom.blog.views import add_new_post_unauth
from custom.blog.views import add_new_post
from custom.blog.views import updatepost
from custom.blog.views import newblog
from custom.blog.views import editblog
from custom.blog.views import userblog
from custom.blog.views import blogpost
from custom.blog.views import newcomment
from custom.blog.views import addnewcomment
from custom.blog.views import addnewcommentunauth
from custom.blog.views import blogcomments
from custom.blog.views import editcomment
from custom.blog.views import usercomments
from custom.blog.feeds import RssSiteNewsFeed, AtomSiteNewsFeed
from custom.chat.views import create_room
from custom.chat.views import join_room
from custom.chat.views import leave_room
from custom.chat.views import post_to_users
from custom.chat.views import post_to_room
from custom.chat.views import send_message
from custom.chat.views import enter_chat
from custom.chat.views import exit_chat
from custom.chat.views import RoomsList
from custom.chat.views import RoomViewSet
from custom.chat.views import MessageViewSet
from custom.chat.views import RoomsList
from custom.chat.views import MessagesList
from custom.chat.views import save_chat_color
from custom.chat.views import read_chat_color
from custom.users.views import editprofile
from custom.users.views import processrivals
from custom.users.views import processfriends
from custom.users.views import user_relationships
from custom.users.views import saveprofile
from custom.users.views import recoverpassword
from custom.users.views import resend_password_link
from custom.users.views import reset
from django.contrib import admin
from custom.chat.views import display_chat

handler404 = 'custom.gui.views.handler404'
handler500 = 'custom.gui.views.handler500'

router = routers.DefaultRouter()
router.register(r'chatrooms', RoomViewSet)
router.register(r'message', MessageViewSet)

urlpatterns = [
    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('', home),
    path('routes/^', include(router.urls)),
    path('add/', forum_new),
    path('topics/<int:topic_id>/attitude/<int:attitude_id>/', forum_add),
    path('topics/<int:topic_id>/emotion/<int:emotion_id>/edit/', forum_edit),
    path('admin/', admin.site.urls),
    path('authenticate/', auth),
    path('authenticate-user/', authentic),
    path('users/', UserList.as_view()),
    path('rooms/', RoomsList.as_view()), 
    path('rooms/<int:pk>/', RoomsList.as_view()),
    path('rooms/<int:creator_id>/', RoomsList.as_view()),
    path('rooms/<is_active>/', RoomsList.as_view()),
    path('chatmessages/', MessagesList.as_view()),
    path('chatmessages/<int:sender_id>/', MessagesList.as_view()),   
    path('chatmessages/<int:room_id>/', MessagesList.as_view()),
    path('chatmessages/<receivers>/', MessagesList.as_view()),
    path('chat/postrooms/', post_to_room),
    path('chat/postusers/', post_to_users),
    path('users/<int:pk>/', UserDetail.as_view()),
    path('user/<int:user_id>/', user_profile),
    path('saveprofile/', saveprofile),
    path('relationships/<int:user_id>/',  user_relationships),
    path('topics/<int:topic_id>/', topics),
    path('activate/<activation_key>/', activate),
    path('reset/<reset_key>/', reset),
    path('api-auth/', include('rest_framework.urls')),      
    path('rest-auth/', include('rest_auth.urls')),
    #path('account/', include('account.urls')),
    #path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('emotions/', EmotionList.as_view()),
    path('attitudes/', AttitudeList.as_view()),
    path('editprofile/', csrf_exempt(editprofile)),
    path('mylh/', csrf_exempt(mylh)),
    path('addnewemotion/', csrf_exempt(newemotion)),
    path('addnewemotionunauth/', csrf_exempt(newemotion_unauth)),
    path('editcomment/<int:comment_id>/', csrf_exempt(editcomment)),
    path('emotions/<int:pk>/', EmotionDetail.as_view()),
    path('attitudes/<int:pk>/', AttitudeDetail.as_view()),
    path('api-token-auth/', csrf_exempt(obtain_jwt_token)),
    path('refresh-token/', csrf_exempt(refresh_jwt_token)),
    path('verify-token/', csrf_exempt(verify_jwt_token)),
    path('logout/', Logout.as_view()),
    path('login/', LoginView.as_view()),
    path('signout/', logout),
    path('statistics/', statistics),
    path('register/', register),
    path('cleanmessages/', cleanmessages),
    path('private/', private),
    path('private/settings/', private_settings),
    path('private/contacts/', private_contacts),
    path('private/unauth/<int:receiver_id>', private_unauth),
    path('private/send/<int:receiver_id>', private),
    path('private/answer/<int:message_id>/', answer_private),
    path('private/answerall/<int:message_id>/', answer_all_private),
    path('private/read/<int:message_id>/', read_private),
    path('private/readall/<int:message_id>/', read_all_private),
    path('chat/create/', create_room),
    path('chat/join/', join_room),
    path('chat/leave/', leave_room),
    path('chat/send/', send_message), 
    path('chat/enter/', enter_chat),
    path('chat/exit/', exit_chat),
    path('chat/savecolor/', save_chat_color),
    path('chat/readcolor/', read_chat_color),
    path('signin/', signin),
    path('topics/', forum),
    path('forum/', forum),
    path('forum/user/<int:user_id>/', user_forum),
    path('mylh/', editprofile),
    path('mylhavatar/', editprofile),
    path('settings/<int:user_id>/', mylh_settings),
    path('blog/', blog),
    path('blogs/', blog),
    path('search/', search),
    path('registernew/', registernew),
    path('newmessage/', csrf_exempt(newmessage)),
    path('editemotion/', editemotion),
    path('newmessageunauth/', csrf_exempt(newmessage_unauth)),
    path('outgoing/', csrf_exempt(outgoing_messages)),
    path('incoming/', csrf_exempt(incoming_messages)),
    path('messages/<int:sender_id>/', incoming_user_messages),
    path('blog/edit/<int:post_id>/', editblog),
    path('blog/comments/user/<int:user_id>/', usercomments),
    path('blog/new/', newblog),
    path('blog/add/', addnewblog),
    path('addnewblog/', addnewblog),
    path('addnewblogunauth/', addnewblogunauth),
    path('updatepost/', updatepost),
    path('addnewcomment/', addnewcomment),
    path('addnewcommentunauth/', addnewcommentunauth),
    path('addnewpostunauth/', add_new_post_unauth),
    path('addnewpost/', add_new_post),
    path('changepassword/', changepassword),
    path('blogpost/<int:post_id>/', blogpost),
    path('blog/user/<int:user_id>/', userblog),
    path('blogcomment/<int:post_id>/', newcomment),
    path('blog/<int:post_id>/', blogcomments),
    path('blog/<int:post_id>/comments/', blogcomments),
    path('recoverpassword/', resend_password_link),
    path('updatepassword/', recoverpassword),
    path('resendactivationbyuser/', resendactivationbyuser),
    path('resendactivationbyuser/<int:user_id>/', resend_activation_by_userid),
    path('processrivals/', processrivals),
    path('processfriends/', processfriends),
    path('addnewfriend/', addnewfriend),
    path('addnewenemy/', addnewenemy),
    path('rss/', RssSiteNewsFeed()),
    path('atom/', AtomSiteNewsFeed()),
    path('chat/', display_chat),
]

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from registration_api import utils
# Datetime related imports
from datetime import datetime
from datetime import date
from datetime import time
from datetime import tzinfo


# Email imports
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# smtp imports
import smtplib
from smtplib import SMTPRecipientsRefused
import string
import codecs
import random
import json
import os
import re

import registration_api
from custom.utils.models import Logger
from custom.users.models import Profile
from custom.users.signals import user_needs_recovery
from custom.users.signals import user_resend_activation
from custom.users.signals import user_send_reset_password_link
from custom.meta.models import ProfileMetaProp
from custom.users.mail import Gmail
from settings import settings

@receiver(user_send_reset_password_link, sender=User)
def reset_password_link(sender, instance, **kwargs):
    try:
        reset_key = utils.create_activation_key(instance)
        link = settings.BASE_URL+'/reset/%s'%reset_key
        user_profile = instance.profile
        user_profile.password_recovery_key = reset_key
        user_profile.save()

        timeNow = datetime.now()

        profile = ProfileMetaProp.objects.get(pk=1)
        FROM = '<strong>Любовь и Ненависть'
        USER = profile.user_name
        PASSWORD = profile.password
        PORT = profile.smtp_port
        SERVER = profile.smtp_server
        TO = instance.profile.email
        SUBJECT = 'Восстановление доступа'
          
        MESSAGE = MIMEMultipart('alternative')
        MESSAGE['subject'] = SUBJECT
        MESSAGE['To'] = TO
        MESSAGE['From'] = "{}".format(FROM)
        MESSAGE.preamble = """
                Your mail reader does not support the report format.
                Please visit us <a href="http://www.divorcesus.com">online</a>!"""
 
        f = codecs.open("templates/activate_inline.html", 'r')
        mess = str(f.read())
        mess = str.replace(mess, '[greeting]', 'Приветствуем Вас на ЛХ,')
        mess = str.replace(mess, '[greeting_statement]', 'Нажмите на кнопку ниже для восстановления доступа.')
        mess = str.replace(mess, '[greeting_link]','Восстановить Пароль')
        mess = str.replace(mess, '[greeting_sent]', 'Это сообщение было послано на адрес')
        mess = str.replace(mess, '[greeting_global_link]', 'Любовь и Ненависть')
        mess = str.replace(mess, '[greeting_locale]', 'Москва, Российская Федерация')
        mess = str.replace(mess, '[First Name]', instance.username)
        mess = str.replace(mess, '[message]', 'Восстановление Доступа')
        mess = str.replace(mess,'email_address@email.com', instance.profile.email)
        mess = str.replace(mess,'[link]', link)


        HTML_BODY  = MIMEText(mess.encode('utf-8'), 'html','utf-8')

        MESSAGE.attach(HTML_BODY)
        msg = MESSAGE.as_string()

        server = smtplib.SMTP(SERVER+':'+PORT)
        server.ehlo()
        server.starttls()
        server.login(USER, PASSWORD)
        server.sendmail(FROM, TO, msg)
        server.quit()

        instance.profile.activation_key = activation_key
        instance.profile.save()
        instance.save()
    except Exception as R:
        log = Logger(log='Failed resetting {}'.format(str(R)))
        log.save()

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
   pass


##########################
## Recover User Profile ##
##########################
@receiver(user_needs_recovery, sender=User)
def recover_profile(sender, instance, request, email,**kwargs):
    user = User.objects.get(email=email)
    mess = 'Welcome to Gringerg & Segal.'

    try:
        member = Profile.objects.get(id=int(user.id))
    except Exception as R:
        member = Profile.objects.get(id=int(instance.id))


    try:
        profile = ProfileMetaProp.objects.get(pk=1)
        FROM = 'Love and Hate <info@lovehate.io>'
        USER = profile.user_name
        PASSWORD = profile.password
        PORT = profile.smtp_port
        SERVER = profile.smtp_server
        TO = email
        f = codecs.open("templates/recover_password.html", 'r')
        m = f.read()
        mess = m
        mess = str.replace(mess, '[reset_link]', link)
        mess = str.replace(mess, '[email]', user.email)
        mess = str.replace(mess, '[first_name]', user.first_name)

        SUBJECT = 'Account recovery notification for %s'%user.username
        message = mess

        MESSAGE = MIMEMultipart('alternative')
        MESSAGE['subject'] = SUBJECT
        MESSAGE['To'] = TO
        MESSAGE['From'] = FROM
        MESSAGE.preamble = """
                Your mail reader does not support the report format.
                Please visit us <a href="http://www.mysite.com">online</a>!"""

        HTML_BODY  = MIMEText(message, 'html','utf-8')
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.


        MESSAGE.attach(HTML_BODY)
        msg = MESSAGE.as_string()
        server = smtplib.SMTP_SSL(SERVER, 465)
        server.ehlo()
        server.starttls()
        server.login(USER,PASSWORD)
        server.sendmail(FROM, TO, msg)
        server.quit()
  #      log_new_user.send(sender='create_profile', message='created new user', level=1)
#        raise ForceResponse(HttpResponseRedirect(reverse('success',kwargs={'code': 'success'})))

    except SMTPRecipientsRefused:
        pass

    except ObjectDoesNotExist:
        pass


def new_account_notify(instance, email):

    try:


        log = Logger(log='WILL TRY TO NOTIFY ABOUT NEW ACCOUNT')
        log.save()
        max_id= User.objects.all().aggregate(id=Max('id'))
        user = User.objects.get(id=max_id['id'])


        users = User.objects.all()#filter(is_active=True).order_by("-date_joined")[:100]

        usrs = []

        for usr in users:
            if usr.date_joined.day==user.date_joined.day:
               if usr.date_joined.month==user.date_joined.month:
                  if usr.date_joined.year==user.date_joined.year:
                            usrs.append(usr)
        today = len(usrs)

        profile = ProfileMetaProp.objects.get(pk=1)
        FROM = '<strong>Восстановление доступа - Любовь и Ненависть'
        USER = profile.user_name
        PASSWORD = profile.password
        PORT = profile.smtp_port
        SERVER = profile.smtp_server
        TO = email

        if instance.first_name:
           first_name = instance.first_name
        else:
           first_name = user.profile.first_name

        strategy = 'Regular Signup'

        log = Logger(log='SIGNUP USED IS {}'.format(strategy))
        log.save()

        time = str(instance.date_joined.time())
        time = time[0:-7]
        year = instance.date_joined.year
        month = instance.date_joined.month
        day = instance.date_joined.day
    #contstruct the message
        BODY='<html><body><strong>A NEW USER HAS REGISTERED'
        BODY+='</stroing><br/><strong>SERVER</strong> %s'%settings.BASE_URL
        BODY+='</stroing><br/><strong>DATE JOINED </strong> %s-%s-%s %s'%(year,month,day,time)
        BODY+='</stroing><br/><strong>USERNAME</strong> %s'%instance.username
        BODY+='</strong><br/><strong>EMAIL</strong> %s'%instance.email
        BODY+='</strong><br/><strong>FIRST NAME</strong> %s'%first_name
        BODY+='</strong><br/><strong>LAST NAME</strong> %s'%last_name
        BODY+='</strong><br/><strong>SIGNED UP USING</strong> %s'%strategy
        if strategy=='Facebook':
           if facebook_id:
               BODY+='</strong><br/><strong>FACEBOOK ID </strong> %s'%str(facebook_id)
        if strategy=='Google':
           if google_id:
               BODY+='</strong><br/><strong>GOOGLE ID </strong> %s'%str(google_id)

        BODY+='</strong><br/><strong>USER ID </strong> %d'%instance.id
        BODY+='</strong><br/><strong>USER PPROFILE </strong> %s'%settings.BASE_URL+'/'+instance.username
        BODY+='</strong><br/><strong>TOTAL USERS </strong> %s'%str(len(User.objects.all()))
        BODY+='</strong><br/><strong>OF THEM TODAY </strong> %s'%str(today)
        BODY+='</body></html>'
        SUBJECT = 'A new user signed up'
        message = 'Subject: %s\n\n%s' % (SUBJECT, BODY)


        MESSAGE = MIMEMultipart('alternative')
        MESSAGE['subject'] = SUBJECT
        MESSAGE['To'] = TO
        MESSAGE['From'] = FROM
        MESSAGE.preamble = """
                Your mail reader does not support the report format.
                Please visit us <a href="http://www.mysite.com">online</a>!"""

        HTML_BODY  = MIMEText(BODY.encode('utf-8'), 'html','utf-8')
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
        MESSAGE.attach(HTML_BODY)
        msg = MESSAGE.as_string()
        server = smtplib.SMTP(SERVER+':'+PORT)
        server.ehlo()
        server.starttls()
        server.login(USER,PASSWORD)
        server.sendmail(FROM, TO, msg)
        server.quit()

    except SMTPRecipientsRefused:
        pass
    except ObjectDoesNotExist:
        pass
    except Exception as R:
        log = Logger(log='An unexcpected error prevented us frpm sending - {} '+str(R))
        log.save()


@receiver(user_resend_activation, sender=User)
def resend_activation_handler(sender, instance, **kwargs):
    send_activation_link(instance)

def send_activation_link(instance):

    mess = 'Please activate your account.'    
    try:
        activation_key = utils.create_activation_key(instance)
        link = settings.BASE_URL+'/activate/%s'%activation_key
        user_profile = instance.profile
        user_profile.activation_key = activation_key
        user_profile.save()

        timeNow = datetime.now()

        profile = ProfileMetaProp.objects.get(pk=1)
        FROM = '<strong>Любовь и Ненависть'
        USER = profile.user_name
        PASSWORD = profile.password
        PORT = profile.smtp_port
        SERVER = profile.smtp_server
        TO = instance.profile.email
        SUBJECT = 'Активируйте вашу запись'
          
        MESSAGE = MIMEMultipart('alternative')
        MESSAGE['subject'] = SUBJECT
        MESSAGE['To'] = TO
        MESSAGE['From'] = "{}".format(FROM)
        MESSAGE.preamble = """
                Your mail reader does not support the report format.
                Please visit us <a href="http://www.divorcesus.com">online</a>!"""
 
        f = codecs.open("templates/activate_inline.html", 'r')
        mess = str(f.read())
        mess = str.replace(mess, '[greeting]', 'Приветствуем Вас на ЛХ,')
        mess = str.replace(mess, '[greeting_statement]', 'Нажмите на кнопку ниже для активации вашей записи.')
        mess = str.replace(mess, '[greeting_link]','Активировать Учётную Запись')
        mess = str.replace(mess, '[greeting_sent]', 'Это сообщение было послано на адрес')
        mess = str.replace(mess, '[greeting_global_link]', 'Любовь и Ненависть')
        mess = str.replace(mess, '[greeting_locale]', 'Москва, Российская Федерация')
        mess = str.replace(mess, '[First Name]', instance.username)
        mess = str.replace(mess, '[message]', 'Account Activation')
        mess = str.replace(mess,'email_address@email.com', instance.profile.email)
        mess = str.replace(mess,'[link]', link)


        HTML_BODY  = MIMEText(mess.encode('utf-8'), 'html','utf-8')

        MESSAGE.attach(HTML_BODY)
        msg = MESSAGE.as_string()

        server = smtplib.SMTP(SERVER+':'+PORT)
        server.ehlo()
        server.starttls()
        server.login(USER, PASSWORD)
        server.sendmail(FROM, TO, msg)
        server.quit()
        log = Logger(log='MESSAGE SENT WAS {}'.format(msg))
        log.save()
        instance.profile.activation_key = activation_key
        instance.profile.save()
        instance.save()
    except Exception as R:
        log = Logger(log='WE FAILED SENDING ACTIVATION %s'%str(R))
        log.save()

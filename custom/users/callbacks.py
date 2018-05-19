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
from custom.users.signals import user_newsletter_sent
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
    mess = 'Love and Hate <info@lovehate.io>'

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

    except SMTPRecipientsRefused:
        pass

    except ObjectDoesNotExist:
        pass

@receiver(user_resend_activation, sender=User)
def resend_activation_handler(sender, instance, **kwargs):
    send_activation_link(instance)

def send_newsletter(instance):

    mess = 'Please activate your account.'
    try:
        user_profile = instance.profile
        user_profile.activation_key = activation_key
        user_profile.save()

        timeNow = datetime.now()

        profile = ProfileMetaProp.objects.get(pk=1)
        FROM = 'Новости Любви и Ненависти'
        USER = profile.user_name
        PASSWORD = profile.password
        PORT = profile.smtp_port
        SERVER = profile.smtp_server
        TO = instance.profile.email
        SUBJECT = 'Недавние работы на сайте'

        MESSAGE = MIMEMultipart('alternative')
        MESSAGE['subject'] = SUBJECT
        MESSAGE['To'] = TO
        MESSAGE['From'] = "{}".format(FROM)
        MESSAGE.preamble = """   """

        f = codecs.open("templates/nesletter.html", 'r')
        mess = str(f.read())
        mess = str.replace(mess, '[greeting]', '▒~_▒~@иве▒~B▒~A▒~Bв▒~Cем ▒~Rа▒~A на ▒~[Х,')
        mess = str.replace(mess, '[greeting_statement]', '▒~]ажми▒~Bе на кнопк▒~C ниже дл▒~O ак▒~Bива▒~Fии ва▒~Hей запи▒~Aи.')
        mess = str.replace(mess, '[greeting_link]','▒~Pк▒~Bиви▒~@ова▒~B▒~L У▒~G▒~Q▒~Bн▒~C▒~N ▒~Wапи▒~A▒~L')
        mess = str.replace(mess, '[greeting_sent]', 'Э▒~Bо ▒~Aооб▒~Iение б▒~Kло по▒~Aлано на ад▒~@е▒~A')
        mess = str.replace(mess, '[greeting_global_link]', '▒~[▒~Nбов▒~L и ▒~]енави▒~A▒~B▒~L')
        mess = str.replace(mess, '[greeting_locale]', '▒~\о▒~Aква, ▒| о▒~A▒~Aий▒~Aка▒~O Феде▒~@а▒~Fи▒~O')
        mess = str.replace(mess, '[First Name]', instance.username)
        mess = str.replace(mess, '[news_message]', message)
        mess = str.replace(mess, '[message]', 'Newsletter')
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
        log = Logger(log='Failed sending email message - {}'.format(str(R)))
        log.save()


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
        instance.profile.activation_key = activation_key
        instance.profile.save()
        instance.save()
    except Exception as R:
        log = Logger(log='Failed sending email message - {}'.format(str(R)))
        log.save()

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
import urllib2
from smtplib import SMTPRecipientsRefused
import string
import codecs
from StringIO import StringIO
import urllib2
import random
import json
import os
import re

from django.dispatch import receiver
from django.contrib.auth.models import User

from models import Notification
from models import NotificationType
from signals import message_read
from signals import message_sent
from signals import message_deleted
from signals import message_updated
from signals import message_duplicate_to_email
from custom.metaprop.models import ProfileMetaProp
from custom.utils.models import Logger

@receiver(message_deleted,sender=User)
def message_deleted_handler(sender,**kwargs):
    pass


@receiver(message_sent, sender=User)
def message_sent_handler(sender, receiver, message, **kwargs):
    try:
        log = Logger(log='WE SENT A MESSAGE %d %d'%(sender.id, receiver.id))
        log.save() 
        notification = Notification.objects.create(notification_type_id = 1, 
                                                   is_received = False,   
                                                   is_sent = True,
                                                   message = message,
                                                   user = receiver)
    except Exception, R:
        log = Logger(log = 'WE ARE IN SIGNAL AND WE HAVE FAILED '+str(R))
        log.save()

@receiver(message_updated, sender=User)
def message_updated_handler(sender, receiver, message, **kwargs):
    pass


@receiver(message_read, sender=User)
def message_read_handler(sender, receiver, message, **kwargs):
    try:
       notification = Notification.objects.get(message=message)
       notification.is_received = True
       notification.save()
    except Exception, R:
        log = Logger(log = 'WE ARE IN SIGNAL READ MESSAGE AND WE HAVE FAILED '+str(R))
        log.save()


@receiver(message_duplicate_to_email, sender=User)
def message_duplicate_to_email_handler(sender, receiver, message, **kwargs):
    log = Logger(log="WE WANT TO DUPLICATE IT")
    log.save()

    log = Logger(log='WILL SEND ACTIVATION')
    log.save()


    mess = 'Please activate your account.'    
    try:

        profile = ProfileMetaProp.objects.get(pk=1)
        FROM = '<strong>Grinberg & Segal'
        USER = profile.user_name
        PASSWORD = profile.password
        PORT = profile.smtp_port
        SERVER = profile.smtp_server
        TO = receiver.profile.email
        SUBJECT = 'Private message'
          
        MESSAGE = MIMEMultipart('alternative')
        MESSAGE['subject'] = SUBJECT
        MESSAGE['To'] = TO
        MESSAGE['From'] = FROM
        MESSAGE.preamble = """
                Your mail reader does not support the report format.
                Please visit us <a href="http://www.divorcesus.com">online</a>!"""
 
        path = "templates/private_message.html"

        f = codecs.open(path, 'r')

        m = f.read()
        mess = string.replace(m, '[Name]', receiver.first_name+' '+receiver.last_name)
        mess = string.replace(mess, '[sender]', sender.first_name+' '+sender.last_name)
        mess = string.replace(mess,'[title]', message.title)
        mess = string.replace(mess,'[body]', message.body)
        mess = string.replace(mess, '[email_address]', receiver.email)
       
        
        message = mess

        HTML_BODY  = MIMEText(message, 'html','utf-8')
        MESSAGE.attach(HTML_BODY)
        msg = MESSAGE.as_string()
        server = smtplib.SMTP(SERVER+':'+PORT)
        server.ehlo()
        server.starttls()
        server.login(USER, PASSWORD)
        server.sendmail(FROM, TO, msg)
        server.quit()
        log = Logger(log="LET US SEND IT {}")
        log.save()
    except Exception as R:
        log = Logger(log='WE FAILED SENDING PRIVATE MESSAGE  %s'%str(R))
        log.save()

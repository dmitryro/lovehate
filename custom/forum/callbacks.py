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

from django.dispatch import receiver
from django.contrib.auth.models import User

from custom.forum.models import Message
from custom.forum.models import Notification
from custom.forum.models import NotificationType
from custom.forum.signals import message_read
from custom.forum.signals import message_sent
from custom.forum.signals import message_deleted
from custom.forum.signals import message_updated
from custom.forum.signals import message_duplicate_to_email
from custom.meta.models import ProfileMetaProp
from custom.utils.models import Logger

@receiver(message_deleted,sender=User)
def message_deleted_handler(sender,**kwargs):
    pass


@receiver(message_sent, sender=User)
def message_sent_handler(sender, receiver, message, **kwargs):
    try:
        notification = Notification.objects.create(notification_type_id = 1, 
                                                   is_received = False,   
                                                   is_sent = True,
                                                   message = message,
                                                   user = receiver)
    except Exception as R:
        pass

@receiver(message_updated, sender=User)
def message_updated_handler(sender, receiver, message, **kwargs):
    pass


@receiver(message_read, sender=User)
def message_read_handler(sender, receiver, message, **kwargs):
    try:
       notification = Notification.objects.get(message=message)
       notification.is_received = True
       notification.save()
    except Exception as R:
       pass

@receiver(message_duplicate_to_email, sender=User)
def message_duplicate_to_email_handler(sender, receiver, message, **kwargs):
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
        mess = string.replace(mess,'[title]', message.subject)
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
    except Exception as R:
        pass

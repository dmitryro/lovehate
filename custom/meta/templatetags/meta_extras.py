import logging
import re
import sys
from django.template import Library, Node, NodeList, TemplateSyntaxError
from django.utils.encoding import smart_str
from custom.meta.models import MetaProp, ContactMetaProp
from django import template
from django.template.defaultfilters import stringfilter





kw_paster = template.Library()

kw_pat = re.compile(r'^(?P<key>[\w]+)=(?P<value>.+)$')
logger = logging.getLogger('sorl.thumbnail')

register = Library()

"""
 Get the logo meta
"""
@register.simple_tag
def metaprop_meta(key, *args, **kwargs):

    metaproperty = MetaProp.objects.get(id=1)

    if (key==1):
        return metaproperty.title
    elif (key==2):
        return metaproperty.keywords
    elif (key==3):
        return metaproperty.description
    elif (key==4):
        return metaproperty.author
    elif (key==5):
        return metaproperty.analytics
    elif (key==6):
        return metaproperty.h1header
    elif (key==7):
        return metaproperty.content




@register.simple_tag
def contact_metaprop_meta(key, *args, **kwargs):

    metaproperty = ContactMetaProp.objects.get(id=1)


    if (key==0):
        return metaproperty.title
    elif (key==1):
        return metaproperty.address1
    elif (key==2):
        return metaproperty.address2
    elif (key==3):
        return metaproperty.city
    elif (key==4):
        return metaproperty.state
    elif (key==5):
        return metaproperty.zip
    elif (key==6):
        return metaproperty.phone
    elif (key==7):
        return metaproperty.fax
    elif (key==8):
        return metaproperty.hours
    elif (key==9):
        return metaproperty.days
    elif (key==10):
        return metaproperty.note

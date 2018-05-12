from django.template import Library, Node, NodeList, TemplateSyntaxError
from django.utils.encoding import smart_str
from django import template
from django.template.defaultfilters import stringfilter

import logging 
import re
import sys
import html2text
from lxml import html, etree
from django.template import Library, Node, NodeList, TemplateSyntaxError
from django.utils.encoding import smart_str
from django import template
from django.template.defaultfilters import stringfilter
from custom.utils.models import Logger
from custom.forum.models import Message

register = template.Library()
h = html2text.HTML2Text()
kw_pat = re.compile(r'^(?P<key>[\w]+)=(?P<value>.+)$')
logger = logging.getLogger('sorl.thumbnail')

register = Library()

css_cleanup_regex = re.compile('((font|padding|margin)(-[^:]+)?|line-height):\s*[^;]+;')


@register.simple_tag
def private_meta(user_id,  *args, **kwargs):
    """
    Get the messages counts meta
    """
    return "(0)"
    try:
        messages = Message.objects.filter(receiver_id=int(user_id), is_read=False)
        if len(messages) > 0:
            total = "({})".format(len(comments))
        else:
            total = ""
        return total
    except Exception as e:
        logging.error("Unable to calculate totals ...")
        return ""


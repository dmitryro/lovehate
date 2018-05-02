import logging
import re
import sys
from django.template import Library, Node, NodeList, TemplateSyntaxError
from django.utils.encoding import smart_str
from custom.meta.models import MetaProp, ContactMetaProp
from django import template
from django.template.defaultfilters import stringfilter
from custom.utils.models import Logger
from custom.forum.models import Topic
from custom.forum.models import Emotion



kw_paster = template.Library()

kw_pat = re.compile(r'^(?P<key>[\w]+)=(?P<value>.+)$')
logger = logging.getLogger('sorl.thumbnail')

register = Library()


logger = logging.getLogger('sorl.thumbnail')

"""
 Get the topic counts meta
"""
@register.simple_tag
def topic_meta(topic_id, user_id, attitude_id,  *args, **kwargs):
    try:
        log = Logger(log='VALUES WERE {} {} {}'.format(topic_id, user_id, attitude_id))
        log.save()

        emotions = Emotion.objects.filter(topic_id=topic_id, user_id=user_id, attitude_id=attitude_id)
        return len(emotions)
    except Exception as e:
        logging.error("Unable to calculate totals ...")
        return 0

import logging
import re
import sys
from django.template import Library, Node, NodeList, TemplateSyntaxError
from django.utils.encoding import smart_str
from custom.meta.models import MetaProp, ContactMetaProp
from django import template
from django.template.defaultfilters import stringfilter
from custom.utils.models import Logger
from custom.blog.models import Post
from custom.blog.models import Comment



kw_paster = template.Library()

kw_pat = re.compile(r'^(?P<key>[\w]+)=(?P<value>.+)$')
logger = logging.getLogger('sorl.thumbnail')

register = Library()


logger = logging.getLogger('sorl.thumbnail')

"""
 Get the topic counts meta
"""
@register.simple_tag
@register.simple_tag
def post_meta(post_id, attitude_id,  *args, **kwargs):
    try:
        comments = Comment.objects.filter(post_id=int(post_id))
        return len(comments)
    except Exception as e:
        logging.error("Unable to calculate totals ...")
        return 0

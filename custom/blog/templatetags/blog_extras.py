import logging
import re
import sys
import html2text
from lxml import html, etree
from django.template import Library, Node, NodeList, TemplateSyntaxError
from django.utils.encoding import smart_str
from custom.meta.models import MetaProp, ContactMetaProp
from django import template
from django.template.defaultfilters import stringfilter
from custom.utils.models import Logger
from custom.blog.models import Post
from custom.blog.models import Comment
from custom.forum.models import Message

register = template.Library()
h = html2text.HTML2Text()
kw_pat = re.compile(r'^(?P<key>[\w]+)=(?P<value>.+)$')
logger = logging.getLogger('sorl.thumbnail')

register = Library()

css_cleanup_regex = re.compile('((font|padding|margin)(-[^:]+)?|line-height):\s*[^;]+;')

def _cleanup_elements(elem):
    """
    Removes empty elements from HTML (i.e. those without text inside).
    If the tag has a 'style' attribute, we remove the css attributes we don't want.
    """
    if elem.text_content().strip() == '':
        elem.drop_tree()
    else:
        if elem.attrib.has_key('style'):
            elem.attrib['style'] = css_cleanup_regex.sub('', elem.attrib['style'])
        for sub in elem:
            _cleanup_elements(sub)

def cleanup_html(string):
    """
    Makes generated HTML (i.e. ouput from the WYSISYG) look almost decent.
    """
    try:
        elem = html.fromstring(string)
        _cleanup_elements(elem)
        html_string = html.tostring(elem)
        lines = []

        for line in html_string.splitlines():
            line = line.rstrip()
            if line != '': lines.append(line)

        return '\n'.join(lines)

    except etree.XMLSyntaxError:
        return string


@register.simple_tag
def post_meta(post_id, attitude_id,  *args, **kwargs):
    """
    Get the topic counts meta
    """
    
    try:
        comments = Comment.objects.filter(post_id=int(post_id))
        if len(comments) > 0:
            total = "({})".format(len(comments))
        else:
            total = ""
        return total
    except Exception as e:
        logging.error("Unable to calculate totals ...")
        return ""

@register.simple_tag
def incoming_meta(user_id, *args, **kwargs):
    """
    Get the topic counts meta
    """

    try:
        messages = Message.objects.filter(receiver_id=int(user_id), is_read=False)
        return len(messages)
    except Exception as e:
        return 0

@register.simple_tag
def link_meta(link,  *args, **kwargs):
    """
    Get the topic counts meta
    """
    return h.handle("<a href=''>{}</a>".format(link))
    try:
        chunks = link.split(' ')
        result = []
        for l in chunks:
            if l[0:4]=='http' or l[0:3]=='www':
                link_to_append = h.handle(l)
            else:
                link_to_append = l
            result.append(link_to_append)
        res = " ".join(result)
        return res

    except Exception as e:
        logging.error("Unable to produce link ...{}".format(e))
        return link


@register.filter
@stringfilter
def split(string, sep):
    """Return the string split by sep.

    Example usage: {{ value|split:"/" }}
    """
    return string.split(sep)

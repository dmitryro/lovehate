from django.contrib.syndication.views import Feed
from django.utils import feedgenerator
from custom.blog.models import Post
from django.utils.feedgenerator import Atom1Feed
from django.urls import reverse
import datetime

class RssSiteNewsFeed(Feed):
    subject = "Любовь и Ненависть Фид"
    link = "/blog/"
    description = "Любовь и Ненависть Фид"

    def items(self):
        return Post.objects.order_by('-time_published')[:5]

    def item_subject(self, item):
        return item.subject

    def item_description(self, item):
        return item.body


class AtomSiteNewsFeed(RssSiteNewsFeed):
    feed_type = Atom1Feed
    subsubject = RssSiteNewsFeed.description

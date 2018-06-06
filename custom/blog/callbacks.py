from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from custom.blog.signals import post_comment_added
from custom.blog.signals import post_comment_edited
from custom.blog.signals import post_comment_deleted
from custom.blog.models import Comment
from custom.blog.models import Post
from custom.utils.models import Logger

@receiver(post_comment_added, sender=Comment)
def post_comment_added_handler(sender, instance, **kwargs):
    log = Logger(log="New comment posted -- time to check")
    log.save()
    try:
        comment = Comment.objects.get(id=instance.id-1)
        if comment.body == instance.body:
          comment.delete()
    except ObjectDoesNotExist:
        pass     

@receiver(post_comment_edited, sender=Comment)
def post_comment_edited_handler(sender, instance, **kwargs):
    log = Logger(log="Existing comment edited -- time to check")
    log.save()

    try:
        comment = Comment.objects.get(id=instance.id-1)
        if comment.body == instance.body:
            comment.delete()
    except ObjectDoesNotExist:
        pass

@receiver(post_comment_edited, sender=Comment)
def post_comment_deleted_handler(sender, instance, **kwargs):
    log = Logger(log="Existing comment deleted -- time to check")
    log.save()




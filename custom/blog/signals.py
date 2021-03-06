from django.dispatch import Signal

post_comment_added = Signal(providing_args=["comment"])
post_comment_edited = Signal(providing_args=["comment"])
post_comment_deleted = Signal(providing_args=["comment"])


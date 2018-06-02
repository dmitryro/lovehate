from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from custom.chat.signals import user_joined_chat
from custom.chat.signals import user_left_chat
from custom.chat.signals import chat_room_created
from custom.chat.signals import chat_room_terminated
from custom.chat.signals import user_joined_room
from custom.chat.signals import user_left_room


@receiver(user_joined_chat, sender=User)
def user_joined_chat_handler():
    pass


@receiver(user_left_chat, sender=User)
def user_left_chat_handler():
    pass


@receiver(user_joined_room, sender=User)
def user_joined_room_handler():
    pass


@receiver(user_left_room, sender=User)
def user_left_room_handler():
    pass


@receiver(chat_room_created, sender=User)
def chat_room_created_handler():
    pass


@receiver(chat_room_terminated, sender=User)
def chat_room_terminated_handler():
    pass




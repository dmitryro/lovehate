from django.dispatch import Signal

user_joined_chat = Signal(providing_args=["user"])
user_left_chat = Signal(providing_args=["user"])
user_joined_room = Signal(providing_args=["user"])
user_left_room = Signal(providing_args=["user"])
chat_room_created = Signal(providing_args=["user"])
chat_room_terminated = Signal(providing_args=["user"])


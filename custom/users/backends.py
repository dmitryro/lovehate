from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend

class LocalBackend(object):
    def authenticate(self, username=None, password=None):
 
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        pwd_valid = user.check_password(password)
        
        if pwd_valid:
            return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


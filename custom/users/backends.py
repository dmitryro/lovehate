from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib.auth.models import User, check_password
from django.contrib.auth.backends import ModelBackend

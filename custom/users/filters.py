from django.contrib.auth.models import User
import rest_framework_filters as filters
from custom.users.models import Profile

class ProfileFilter(filters.FilterSet):
    username = filters.CharFilter(name='username')
    email = filters.CharFilter(name='email')
    first_name = filters.CharFilter(name='first_name')
    last_name = filters.CharFilter(name='last_name')

    class Meta:
        model = Profile
        fields = ['id', 'username', 'email', 
                  'first_name', 'last_name']

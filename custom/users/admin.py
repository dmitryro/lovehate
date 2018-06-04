from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib import admin
from custom.users.models import Profile
from custom.users.models import Relationship
from custom.users.models import Peer

class CustomUserAdmin(UserAdmin):
    def __init__(self, *args, **kwargs):
        super(UserAdmin,self).__init__(*args, **kwargs)
        UserAdmin.list_display = list(UserAdmin.list_display) + ['id','date_joined', 'last_login','is_active']

    # Function to count objects of each user from another Model (where user is FK)
    def some_function(self, obj):
        return obj.another_model_set.count()

#####################################
#  Register Peer with Django Admin  #
#####################################

class PeerAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['strength',
                                    'relation',
                                    'initiator',
                                    'acceptor',
                         ]}),)

    list_display = ('id', 'strength', 'relation', 'initiator', 'acceptor',)
    list_editable = ('strength', 'relation', 'initiator', 'acceptor',)
    search_fields = ('strength', 'relation', 'initiator', 'acceptor',)


#############################################
#  Register Relationship with Django Admin  #
#############################################

class RelationshipAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['name',
                                    'code']}),)
    list_display = ('id', 'name', 'code',)
    list_editable = ('name', 'code',)
    search_fields = ('name', 'code',)

    class Meta:
         verbose_name = 'Relationship'
         verbose_name_plural = 'Relationship'


########################################
#  Register Profile with Django Admin  #
########################################

class ProfileAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': [
                                    'username',
                                    'email', 
                                    'user',
                                    'is_cleared',
                                    'is_activated',
                                    'bio',
                                    'is_facebook_signup_used',
                                    'is_google_signup_used',
                                    'is_linkedin_signup_used',
                                    'is_username_customized',
                                    'is_twitter_signup_used',
                                    'is_vk_signup_used',
                                    'is_new',
                                    'first_name','last_name',
                                    'phone',
                                    'profile_image_path']}),)

    list_display = ('username', 'username_transliterated', 
                    'user', 'email', 'first_name', 'last_name', 
                    'date_joined', 'is_new',  'bio', 'phone')

#    list_editable = ('username', 'username_transliterated', 
#                     'user', 'email', 'first_name', 'last_name', 
#                     'is_new', 'phone', 'bio')
    search_fields = ('username', 'username_transliterated', 
                     'first_name', 'last_name','email','phone', 
                     'bio')


    class Meta:
         verbose_name = 'User Profile'
         verbose_name_plural = 'User Profiles'


    def __init__(self, *args, **kwargs):
        super(ProfileAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = ('username',  'username_transliterated',
                                   'user', 'email', 'first_name', 'last_name',
                                   'date_joined', 'is_new',  'bio', 'phone')


admin.site.register(Relationship, RelationshipAdmin)
admin.site.register(Peer, PeerAdmin)
admin.site.register(Profile,ProfileAdmin)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)

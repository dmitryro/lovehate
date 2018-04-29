from django.contrib import admin
from custom.users.models import Profile

########################################
#  Register Profile with Django Admin  #
########################################

class ProfileAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['username',
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

    list_display = ('id','username','user','email','first_name','last_name','date_joined','is_new', 'bio','phone')

    list_editable = ('username', 'user', 'email', 'first_name', 'last_name', 'is_new', 'phone', 'bio')
    search_fields = ('username', 'first_name', 'last_name','email','phone', 'bio')


    class Meta:
         verbose_name = 'User Profile'
         verbose_name_plural = 'User Profiles'

admin.site.register(Profile,ProfileAdmin)

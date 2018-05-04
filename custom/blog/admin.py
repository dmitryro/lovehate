from django.contrib import admin
from custom.blog.models import Post
########################################
#  Register Post with Django Admin     #
########################################

class PostAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['author',
                                    'subject',
                                    'translit_subject',
                                    'body',
                                    'link',
                                    'attitude',
                                    'rating']}),)

    list_display = ('id','author', 'subject', 'body', 'translit_subject', 'link', 'attitude', 'rating',)
    list_editable = ('author', 'subject', 'body', 'translit_subject', 'link', 'attitude', 'rating',)
    search_fields = ('author', 'subject', 'body', 'translit_subject', 'link', 'attitude', 'rating',)

    class Meta:
         verbose_name = 'Post'
         verbose_name_plural = 'Posts'

admin.site.register(Post, PostAdmin)


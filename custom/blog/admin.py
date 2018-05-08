from django.contrib import admin
from custom.blog.models import Post
from custom.blog.models import Comment
########################################
#  Register Post with Django Admin     #
########################################

class PostAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['author',
                                    'subject',
                                    'translit_subject',
                                    'body',
                                    'link',
                                    'link_two',
                                    'link_three',
                                    'link_four',
                                    'link_five',
                                    'ip_address',
                                    'attitude',
                                    'rating']}),)

    list_display = ('id','author', 'subject', 'body', 'translit_subject', 
                    'link',  'link_two',
                    'link_three','link_four','link_five',
                    'attitude', 'rating', 'ip_address',)
    list_editable = ('author', 'subject', 'body', 'translit_subject', 
                     'link',  'link_two',
                    'link_three','link_four','link_five', 
                    'attitude', 'rating', 'ip_address',)
    search_fields = ('author', 'subject', 'body', 'translit_subject', 
                     'link',  'link_two',
                     'link_three','link_four','link_five',
                     'attitude', 'rating', 'ip_address',)

    class Meta:
         verbose_name = 'Post'
         verbose_name_plural = 'Posts'

class CommentAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['author',
                                    'title',
                                    'post',
                                    'body',
                                    'link',
                                    'ip_address',
                                    'rating',
                                    'attitude',]}),)

    list_display = ('id','author', 'title', 'body', 'ip_address', 'link', 'attitude', 'rating',)
    list_editable = ('author', 'title', 'body', 'link', 'ip_address', 'attitude', 'rating',)
    search_fields = ('author', 'title', 'body', 'link', 'ip_address', 'attitude', 'rating',)


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)

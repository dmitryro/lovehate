import rest_framework_filters as filters

from custom.blog.models import Post 


class PostFilter(filters.FilterSet):
    id = filters.CharFilter(name='id')
    subject = filters.CharFilter(name='subject')
    statement = filters.CharFilter(name='body')
    time_published = filters.CharFilter(name='time_published')
    author = filters.CharFilter(name='author')
    translit_subject = filters.CharFilter(name='translit_subject')

    class Meta:
        model = Post
        fields = ['id', 'subject', 'author', 'time_published', 'body',
                  'translit_subject',]

from django.db import models
from django.contrib.auth.models import User
from custom.forum.models import Attitude

class Post(models.Model):
    link = models.CharField(max_length=1850, blank=True, null=True)
    link_two = models.CharField(max_length=1850, blank=True, null=True)
    link_three = models.CharField(max_length=1850, blank=True, null=True)
    link_four = models.CharField(max_length=1850, blank=True, null=True) 
    link_five = models.CharField(max_length=1850, blank=True, null=True)
    author = models.ForeignKey(User, blank=True, null=True,  on_delete=models.CASCADE)
    subject = models.CharField(max_length=1250, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    time_published = models.DateTimeField(auto_now_add=True)
    time_last_commented = models.DateTimeField(blank=True, null=True)
    time_last_edited = models.DateTimeField(blank=True, null=True)
    rating =  models.FloatField(default=0, blank=True, null=True)
    attitude = models.ForeignKey(Attitude, blank=True, null=True, on_delete=models.CASCADE)
    attached_image_path = models.CharField(max_length=1450, blank=True, null=True) 
    translit_subject = models.CharField(max_length=1250,
                                        blank=True,
                                        null=True)
    ip_address = models.CharField(max_length=40,
                                  blank=True,
                                  null=True)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


    def __str__(self):
        return self.subject


    @property
    def author_nick(self):
        return self.author.profile.username

    @property
    def long_article(self):
        return len(self.body) > 334

    @property
    def teaser_lines(self):
        body = str(self.body)
        if len(body) > 334:
            teaser = "{}...".format(body[:330])
        else:
            teaser = body
        return teaser.splitlines()

    @property
    def date_time_published(self):
        dt = str(self.time_published)
        year = dt[0:4]
        month = dt[5:7]
        day = dt[8:10]
        return "{}/{}/{} {}:{}:{}".format(day,
                                          month,
                                          year,
                                          self.time_published.hour,
                                          self.time_published.minute,
                                          self.time_published.second)
    @property
    def body_lines(self):
        return self.body.splitlines()


    def get_absolute_url(self):
        return '/'+self.subject+'/'

class Comment(models.Model):
    title = models.CharField(max_length=250, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    attitude = models.ForeignKey(Attitude, blank=True, null=True, on_delete=models.CASCADE)
    link = models.CharField(max_length=1850, blank=True, null=True)
    author = models.ForeignKey(User, blank=True, null=True,  on_delete=models.CASCADE)
    post = models.ForeignKey(Post, blank=True, null=True,  on_delete=models.CASCADE)
    rating =  models.FloatField(default=0, blank=True, null=True)
    time_published = models.DateTimeField(auto_now_add=True)
    time_last_edited = models.DateTimeField(blank=True, null=True)
    ip_address = models.CharField(max_length=40,
                                  blank=True,
                                  null=True)
    
    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        if self.title:
              title = self.title
        else:
              title = 'unknown'
        return title

    @property
    def author_nick(self):
        return self.author.profile.username
    
    @property
    def body_len(self):
        return len(self.body.splitlines())

    @property
    def body_lines(self):
        return self.body.splitlines()

    @property
    def date_time_published(self):
        dt = str(self.time_published)
        year = dt[0:4]
        month = dt[5:7]
        day = dt[8:10]
        return "{}/{}/{} {}:{}:{}".format(day,
                                          month,
                                          year,
                                          self.time_published.hour,
                                          self.time_published.minute,
                                          self.time_published.second)




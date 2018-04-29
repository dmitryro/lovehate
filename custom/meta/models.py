from django.db import models
from django.contrib import admin
from django import forms


# This model is for basic html meta settings
class ContactMetaProp(models.Model):
    title = models.CharField(max_length=150)
    address1 = models.CharField(max_length=150)
    address2 = models.CharField(max_length=150,blank=True, null=True)
    city =  models.CharField(max_length=150)
    zip = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    fax = models.CharField(max_length=20)
    hours = models.CharField(max_length=200)
    days =  models.CharField(max_length=200)
    note = models.CharField(max_length=1500,blank=True, null=True)
    class Meta:
        verbose_name = 'contact meta property'
        verbose_name_plural = 'contact meta properties'


class ProfileMetaProp(models.Model):
    title = models.CharField(max_length=150,blank=True, null=True)
    email = models.EmailField()
    from_email = models.EmailField()
    to_email = models.EmailField()
    to_email_secondary = models.EmailField()
    to_email_third = models.EmailField()
    smtp_server =  models.CharField(max_length=150)
    smtp_port =  models.CharField(max_length=10)
    user_name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    message = models.CharField(max_length=2500,blank=True, null=True)
    class Meta:
        verbose_name = 'profile meta property'
        verbose_name_plural = 'profile meta properties'


class MetaProp(models.Model):
    title = models.CharField(max_length=140)
    keywords = models.CharField(max_length=1600)
    description  =  models.TextField(max_length=1500)
    author  =  models.CharField(max_length=140)
    analytics =  models.CharField(max_length=60)
    h1header = models.CharField(max_length=140,null=True,blank=True)
    content = models.TextField(max_length=1600,null=True,blank=True)

    # meta class
    class Meta:
        verbose_name = 'seo meta property'
        verbose_name_plural = 'seo meta properties'


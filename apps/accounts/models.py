from __future__ import unicode_literals
from django.contrib import messages
from django.db import models
import bcrypt
import datetime
import re
DATE_REGEX = re.compile (r'^[0-9]+-[0-9]+-[0-9]+$')

# EMAIL_REGEX = re.compile (r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register(self, userInfo, request):
        passFlag = True
        if len(userInfo['name']) < 8:
            messages.warning(request, 'Name is not long enough.')
            passFlag = False
        if len(userInfo['username']) < 8:
            messages.warning(request, 'Username is not long enough.')
            passFlag = False
        if len(userInfo['password']) < 8:
            messages.warning(request, 'Password is not long enough.')
            passFlag = False
        if userInfo['password'] != userInfo['confirm_password']:
            messages.warning(request, 'Password match not confirmed.')
            passFlag = False
        if User.objects.filter(username__exact= userInfo['username']):
            messages.error(request, "Invalid Username.")
            passFlag = False

        if passFlag:
        	messages.error(request, "Successful Registration!")
        	hashed = bcrypt.hashpw(userInfo['password'].encode(), bcrypt.gensalt())
        	user = self.create(name = userInfo['name'], username = userInfo['username'], password = hashed)
        return passFlag

    def login(self, userInfo, request):
        passFlag = True
        if User.objects.filter(username = userInfo['username']):
            hashed = User.objects.get(username = userInfo['username']).password
            hashed = hashed.encode('utf-8')
            password = userInfo['password']
            password = password.encode('utf-8')
            if bcrypt.hashpw(password, hashed) == hashed:
                passFlag = True
            else:
                messages.warning(request, "Unsuccessful login")
                passFlag = False
        else:
            messages.warning(request, "Unsuccessful login")
            passFlag = False
        return passFlag

class TripManager(models.Manager):
    def register(self, tripInfo, request):
        passFlag = True
        if len(tripInfo['title']) < 3:
            messages.warning(request, 'Destination is not long enough.')
            passFlag = False
        if len(tripInfo['title']) < 8:
            messages.warning(request, 'Description is not long enough.')
            passFlag = False
        if len(tripInfo['travelDateTo']) < 3:
            messages.warning(request, 'Incorrect To date.')
            passFlag = False
        if not DATE_REGEX.match(tripInfo['travelDateTo']):
            messages.warning(request, 'Incorrect To date.')
            passFlag = False
        if len(tripInfo['travelDateFrom']) < 3:
            messages.warning(request, 'Incorrect From date.')
            passFlag = False
        if not DATE_REGEX.match(tripInfo['travelDateFrom']):
            messages.warning(request, 'Incorrect To date.')
            passFlag = False
        if tripInfo['travelDateFrom'] > tripInfo['travelDateTo']:
            messages.warning(request, 'Date To must be after Date From.')
            passFlag = False
        if Destination.objects.filter(title__exact= tripInfo['title']):
            messages.error(request, "Invalid Username.")
            passFlag = False

        if passFlag:
            messages.error(request, "Successful Registration!")
            # user = self.create(name = userInfo['name'], username = userInfo['username'], password = hashed)
        return passFlag


class User(models.Model):
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    userManager = UserManager()
    objects = models.Manager()

class Destination(models.Model):
    planned_by_id = models.ForeignKey(User)
    title = models.CharField(max_length=200, default='title')
    description = models.TextField(max_length=1000)
    travelDateFrom =  models.DateField() #(), default=datetime.date.today)
    travelDateTo =  models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tripManager = TripManager()
    objects = models.Manager()

class Joined(models.Model):
    joined_by_id = models.ManyToManyField(User)
    destination_id = models.ManyToManyField(Destination)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
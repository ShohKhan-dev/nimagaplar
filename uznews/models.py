from enum import unique
from django.db import models
# from django.contrib.auth.models import User

# Create your models here. 

from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.utils import timezone

from django.utils.translation import gettext as _


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """

    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError(_('Users must have an username'))

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    telegram_name = models.CharField(max_length=250, null=True, blank=True)
    email = models.EmailField(max_length=250, unique=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    receive_notification = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'


class RandomNumber(models.Model):
    numb = models.IntegerField()
   




class Keywords(models.Model):
    word = models.CharField(max_length=125)
    users = models.ManyToManyField(User, related_name='keywords')
    created_at = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        ordering = ('-created_at',)


    def __str__(self):
        return self.word






class WatchList(models.Model):
    word = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.word
    
class IgnoreList(models.Model):
    word = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.word


class WaitList(models.Model):
    word = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.word



class News(models.Model):
    title = models.CharField(max_length=500)
    link = models.CharField(max_length=500, unique=True)
    views = models.IntegerField()
    category = models.CharField(max_length=25, null=False, blank=True)
    posted_at = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=20)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-posted_at',)
    






# class Notification(models.Model):

#     to_user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)

#     is_read = models.BooleanField(default=False)

#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['-created_at']
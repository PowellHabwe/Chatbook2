from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import User
# Create your models here.

from mimetypes import guess_type
import uuid
class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    avatar = models.ImageField(null=True, default="avatar.svg")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host =  models.ForeignKey(User, on_delete=models.SET_NULL, null = True) 
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null = True) 
    name = models.CharField(max_length=200)
    description = models.TextField(null = True, blank=True)
    participants = models.ManyToManyField(User, related_name = 'participants', blank = True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)  
    body = models.TextField()      
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]

# class Post(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     owner =  models.ForeignKey(User, on_delete=models.SET_NULL, null = True) 
#     user = models.CharField(max_length=50)
#     image = models.ImageField(upload_to='post_images')
#     caption = models.TextField()
#     created_at = models.DateTimeField(default=datetime.now)
#     no_of_likes = models.IntegerField(default = 0)

#     def __str__(self):
#         return self.caption


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    host =  models.ForeignKey(User, on_delete=models.SET_NULL, null = True) 
    image = models.FileField(upload_to='post_images', null=False,blank=False)
    video = models.FileField(upload_to="video/%y",  null=False,blank=False)
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default = 0)

    def __str__(self):
        return self.caption

class LikePost(models.Model):
    post_id = models.CharField(max_length=100)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    # follower = models.ForeignKey(User,  on_delete=models.SET_NULL)
    # user = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.follower

class Comment(models.Model):
    name =models.CharField(max_length=50)
    date_added = models.DateField(auto_now_add=True)
    post = models.ForeignKey('Post',related_name="comments", on_delete=models.CASCADE)
    body = models.TextField()

    def __str__(self):
        return self.name
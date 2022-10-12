from django.contrib import admin

# Register your models here.
from .models import Room,Comment, Topic, Message, User, Post, LikePost, FollowersCount

admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(FollowersCount)

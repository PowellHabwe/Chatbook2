from django.forms import ModelForm
from django import forms
from .models import Room, User, Post, Comment
from django.contrib.auth.forms import UserCreationForm

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar','name', 'username', 'email', 'bio']        

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'

class CommentForm(ModelForm):
    # content = forms.CharField(widget=forms.Textarea(attrs = {
    #     'rows': '4',
    # }))
    class Meta:
        model = Comment
        fields = ['body', 'name']
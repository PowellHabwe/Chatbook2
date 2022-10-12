from imp import PKG_DIRECTORY
from django.shortcuts import render,redirect
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Room, Topic, Message, User, Post, LikePost, FollowersCount
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import RoomForm, UserForm, MyUserCreationForm, PostForm, CommentForm

from itertools import chain
import random
# Create your views here.
# rooms = [
#     {'id': 1, 'name': 'Lets learn Python'},
#     {'id': 2, 'name': 'Lets learn Java'},
#     {'id': 3, 'name': 'Lets learn Css'},
# ]

def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'The user does not exist.')

        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'The username or password does not exist.')    


    context = {'page':page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form  = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.username = user.username.lower()  
            user.save()    
            login(request, user)  
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')

    return render(request, 'base/login_register.html', {'form':form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q) |
        Q(description__icontains = q)
        )
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms':rooms, 'topics':topics, 'room_count':room_count, 'room_messages':room_messages}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room=room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
        
    context = {'room': room, 'room_messages':room_messages, 'participants':participants}        
    return render(request, 'base/room.html', context)

@login_required(login_url='login')
def userProfile(request, pk):
    user = User.objects.get(id = pk)

    rooms = user.room_set.all()
    user_posts = user.post_set.all()
    follower = user.email
    if FollowersCount.objects.filter(follower=follower, user=request.user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'
    # if FollowersCount.objects.filter(follower=follower, user=pk).first():
    #     button_text = 'Unfollow'
    # else:
    #     button_text = 'Follow'
    user_following = len(FollowersCount.objects.filter(user=pk))
    user_followers = len(FollowersCount.objects.filter(follower = request.user))
    post_length = len(user_posts)
    room_length = len(rooms)
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {
        'user':user,
        'button_text':button_text, 
        'user_posts':user_posts,
        'post_length':post_length,
        'room_length':room_length,
        'rooms':rooms,
        'room_messages': room_messages,
        'topics':topics,
        'user_followers':user_followers,
        'user_following':user_following,
        }
    return render(request, 'base/profile.html', context)



# @login_required(login_url='login')
# def userProfile(request, pk):
#     user = User.objects.get(id = pk)
#     rooms = user.room_set.all()
#     user_posts = user.post_set.all()
#     follower = user.username
#     if FollowersCount.objects.filter(follower=user).first():
#         button_text = 'Unfollow'
#     else:
#         button_text = 'Follow'
#     # if FollowersCount.objects.filter(follower=follower, user=pk).first():
#     #     button_text = 'Unfollow'
#     # else:
#     #     button_text = 'Follow'
#     user_following = len(FollowersCount.objects.filter(user=pk))
#     user_followers = len(FollowersCount.objects.filter(follower = pk))
#     post_length = len(user_posts)
#     room_length = len(rooms)
#     room_messages = user.message_set.all()
#     topics = Topic.objects.all()
#     context = {
#         'user':user,
#         'button_text':button_text, 
#         'user_posts':user_posts,
#         'post_length':post_length,
#         'room_length':room_length,
#         'rooms':rooms,
#         'room_messages': room_messages,
#         'topics':topics,
#         'user_followers':user_followers,
#         'user_following':user_following,
#         }
#     return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm() 
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),

        )
        return redirect('home')

    context = {'form': form, 'topics':topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host :
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
         topic_name = request.POST.get('topic')
         topic, created = Topic.objects.get_or_create(name=topic_name)
         room.name = request.POST.get('name')
         room.topic = topic
         room.description = request.POST.get('description')
         room.save()
         return redirect('home')

    context = {'form': form, 'topics':topics, 'room':room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host :
        return HttpResponse('You are not allowed here!')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user :
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':message})    

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance = user)

    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES, instance = user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk = user.id)
    return render(request, 'base/update-user.html', {'form':form})

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics':topics})

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages':room_messages})

# POSTS
@login_required(login_url='login')
def index(request):
    user_object = User.objects.get(username=request.user.username)

    feed_posts = Post.objects.all()
    # user_following_list = []
    # feed = []

    user_following = FollowersCount.objects.filter(follower = request.user.username)

    # for users in user_following:
    #     user_following_list.append(users.user)
    # for usernames in user_following_list:
    #     feed_lists = Post.objects.filter(user=usernames)
    #     feed.append(feed_list)

    # feed_list = list(chain(*feed))
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username = user.user)
        user_following_all.append(user_list)
    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)

    final_suggestions_list = [x for x in list(new_suggestions_list) if (x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []
    for users in final_suggestions_list:
        username_profile.append(users.id)
    for ids in username_profile:
        profile_lists = User.objects.filter(id = ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))
    return render(request, 'base/index.html', {'title': 'index','suggestions_username_profile_list':suggestions_username_profile_list[:4], 'posts':feed_posts}) 


# @login_required(login_url='login')
# def upload(request):
#     if request.method == 'POST':
#         user =  request.user,
#         image = request.FILES.get('image_upload')
#         caption = request.POST['caption']
#         new_post = Post.objects.create(user=user, image=image, caption=caption)
#         new_post.save()

#         return redirect('index')
#     else:
#         return redirect('index')


@login_required(login_url='login')
def upload(request):
    form = PostForm() 
    if request.method == 'POST':
        Post.objects.create(
            host = request.user,
            image = request.FILES.get('image_upload'),
            video = request.FILES.get('video_upload'),
            caption = request.POST.get('caption'),

        )
        return redirect('index_home')

    context = {'form': form}
    return render(request, 'base/index-home.html', context)

@login_required(login_url='login')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id= post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()

        post.no_of_likes = post.no_of_likes+1
        post.save()

        return redirect('index_home')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('index_home')

@login_required(login_url='login')
def follow(request, pk):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.user

        if FollowersCount.objects.filter(follower =follower, user= user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('index')
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('index')
    else: 
        return redirect('index')

# @login_required(login_url='login')
# def follow(request, pk):
#     user = User.objects.get(id = pk)
#     if request.method == 'POST':
#         follower = request.POST['follower']
#         # follower =user
#         user = request.user

#         if FollowersCount.objects.filter(follower =follower, user= user).first():
#             delete_follower = FollowersCount.objects.get(follower=follower, user=user)
#             delete_follower.delete()
#             return redirect('index')
#         else:
#             new_follower = FollowersCount.objects.create(follower=follower, user=user)
#             new_follower.save()
#             return redirect('index')
#     else: 
#         return redirect('index')

# @login_required(login_url='login')
# def search(request):

#     # user_object = User.objects.get(username = request.user.username)
#     # user_profile = User.objects.get(user = user_object)

#     if request.method == 'POST':
#         username == request.GET.username
#         username_object = User.objects.filter(username__icontains = username)
#         username_profile = []
#         username_profile_list = []

#         for users in username_object:
#             username_profile.append(users.id)

#         for ids in username_profile:
#             profile_lists=User.objects.filter(id=ids)
#             username_profile_list.append(profile_lists)
#         username_profile_list = list(chain(*username_profile_list))
#     return render(request, 'base/search.html', {'username_profile_list':username_profile_list})

def search(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    username = User.objects.filter(name__icontains=q)
    return render(request, 'base/search.html', {'username':username})


@login_required(login_url='login')
def deletePost(request, pk):
    post = Post.objects.get(id=pk)
    if request.user != post.host :
        return HttpResponse('You are not allowed here!')
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'base/delete_post.html', {'obj':post})


@login_required(login_url='login')
def postDetail(request, pk):
    post = Post.objects.get(id=pk)
    context = {
        'post':post, 

        }
    return render(request, 'base/postdetail.html', context)

@login_required(login_url='login')
def postDetail1(request, pk):
    form = CommentForm()
    post = Post.objects.get(id=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.post = post
            obj.save()

            return redirect('index_home')
    else:
        CommentForm()
    context = {
        'post':post,
        'form':form

        }
    return render(request, 'base/postdetail1.html', context)


@login_required(login_url='login')
def indexHome(request):
    return render(request, 'base/indexhome.html')


@login_required(login_url='login')
def snakeGame(request):
    return render(request, 'base/game.html')


# POSTS
@login_required(login_url='login')
def indexHome(request):
    user_object = User.objects.get(username=request.user.username)

    feed_posts = Post.objects.all()
    # user_following_list = []
    # feed = []

    user_following = FollowersCount.objects.filter(follower = request.user.username)
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q) |
        Q(description__icontains = q)
        )
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username = user.user)
        user_following_all.append(user_list)
    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)

    final_suggestions_list = [x for x in list(new_suggestions_list) if (x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []
    for users in final_suggestions_list:
        username_profile.append(users.id)
    for ids in username_profile:
        profile_lists = User.objects.filter(id = ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))
    return render(request, 'base/indexhome.html', {
        'title': 'index',
        'rooms':rooms,
        'topics':topics,
        'room_count':room_count,
        'room_messages':room_messages,
        'suggestions_username_profile_list':suggestions_username_profile_list[:4],
        'posts':feed_posts}) 


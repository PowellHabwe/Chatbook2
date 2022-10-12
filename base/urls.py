from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),


    path('index/', views.index, name="index"),
    path('index-home/', views.indexHome, name="index_home"),
    path('index/upload', views.upload, name="upload"),
    path('index-home/upload', views.upload, name="upload"),
    path('index/search', views.search, name="search"),
    path('profile/<str:pk>/follow', views.follow, name="follow"),
    path('delete-post/<str:pk>/', views.deletePost, name="delete-post"),
    # path('post/<str:pk>/', views.postDetail, name="post_detail"),
    path('postdetail/<str:pk>/', views.postDetail1, name="post_detail1"),
    # path('index/follow', views.follow, name="follow"),
    path('index/like_post', views.like_post, name="like_post"),
    path('index-home/like_post', views.like_post, name="like_post"),

    path('', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

    path('create-room', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
    path('update-user/',  views.updateUser, name="update-user"),
    path('topics/',  views.topicsPage, name="topics"),
    path('activity/',  views.activityPage, name="activity"),

    path('snake/',  views.snakeGame, name="snake"),

]

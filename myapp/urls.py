from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import logout
from django.shortcuts import redirect

def red_logout(request):
    logout(request)
    return redirect('/')

urlpatterns = [
    path('', views.login_page, name='login_page'),# login page as default
    #path('', views.list_page, name='home'), 
    path('home/', views.list_page, name='home'), 
    path('user/', views.user_page, name='user_page'),
    path('edit-profile/', views.edit_account, name='edit_profile'),
    path('list/', views.list_page, name='list_page'),
    path('followers/', views.followers_page, name='followers_page'),
    path('following/', views.following_page, name='following_page'),
    path('search/', views.search_page, name='search_page'),
    path('game/<int:game_id>/', views.game_info_page, name='game_info_page'),
    path('add-to-list/', views.add_game_to_list, name='add_game_to_list'),
    path('followers/', views.followers_page, name='followers'),
    path('following/', views.following_page, name='following'),
    path('followers/search/', views.search_followers, name='search_followers'),
    path('following/search/', views.search_following, name='search_following'),
    path('unfollow/<str:username>/', views.unfollow_user, name='unfollow'),
    path('follow_back/<str:username>/', views.follow_back_user, name='follow_back'),
    path('profile/', views.profile_page, name='profile_page'),
    path('logout/', red_logout, name='logout'),
    path('signup/', views.signup_page, name='signup_page'),

]
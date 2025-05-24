from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLoginView
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('signup/', views.signup, name='signup'),
    #path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', views.public_profile, name='public_profile'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('toggle-follow/<str:username>/', views.toggle_follow, name='toggle_follow'),


    path('posts/', views.post_list, name='post_list'),
    path('posts/create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('unlike/<int:post_id>/', views.unlike_post, name='unlike_post'),

    path('follow/<str:username>/', views.toggle_follow, name='toggle_follow'),
    path('follow_user/<int:user_id>/', views.follow_user, name='follow_user'),
    path('users/follow/<str:username>/', views.toggle_follow, name='toggle_follow'),


    path('password_change/',
         auth_views.PasswordChangeView.as_view(template_name='users/password_change.html'),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),
         name='password_change_done'),
]

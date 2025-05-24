from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import SignupForm

from django.views.decorators.http import require_POST
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Post, Comment, Like, Follow, Profile, CustomUser
from .forms import CustomUserCreationForm, PostForm, CommentForm, ProfileForm

User = get_user_model()

# -----------------------
# Authentication Views
# -----------------------

def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto-login after registration
            return redirect('profile')  # redirect to profile or home
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'users/login.html'

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "Logged in successfully.")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

# -----------------------
# Home & Posts
# -----------------------

def home(request):
    posts = Post.objects.all().select_related('author__profile').order_by('-created_at')
    return render(request, 'users/home.html', {'posts': posts})

@login_required
def post_list(request):
    posts = Post.objects.all().select_related('author__profile').prefetch_related('likes')
    return render(request, 'users/post_list.html', {'posts': posts})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).select_related('user')
    liked = post.likes.filter(id=request.user.id).exists()

    return render(request, 'users/post_detail.html', {
        'post': post,
        'comments': comments,
        'liked': liked,
        'form': CommentForm(),
    })

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'users/create_post.html', {'form': form})

# -----------------------
# Likes & Comments
# -----------------------


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()  # Unlike if already liked
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def unlike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.likes.remove(request.user)
    return redirect('post_detail', post_id=post.id)

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
    return redirect('post_detail', post_id=post_id)

# -----------------------
# Profile Views
# -----------------------

@login_required
def public_profile(request, username):
    profile_user = get_object_or_404(CustomUser, username=username)  # ✅ define this properly
    profile = profile_user.profile
    posts = Post.objects.filter(author=profile_user)
    followers = Follow.objects.filter(following=profile_user).select_related('follower')
    following = Follow.objects.filter(follower=profile_user).select_related('following')

    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()

    return render(request, 'users/profile.html', {
        'profile_user': profile_user,
        'profile': profile,
        'posts': posts,
        'followers': followers,
        'following': following,
        'is_following': is_following,
    })


def edit_profile(request):
    user_profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=user_profile)
    return render(request, 'users/edit_profile.html', {'form': form})


# -----------------------
# Follow/Unfollow
# -----------------------

@require_POST
@login_required
def toggle_follow(request, username):
    target_user = get_object_or_404(CustomUser, username=username)

    if target_user == request.user:
        return JsonResponse({'error': 'You cannot follow yourself.'}, status=400)

    follow, created = Follow.objects.get_or_create(follower=request.user, following=target_user)

    if not created:
        follow.delete()
        is_following = False
    else:
        is_following = True

    follower_count = Follow.objects.filter(following=target_user).count()
    following_count = Follow.objects.filter(follower=target_user).count()

    return JsonResponse({
        'is_following': is_following,
        'follower_count': follower_count,
        'following_count': following_count,
    })



@login_required
def follow_user(request, user_id):
    if request.method == 'POST':
        target_user = get_object_or_404(CustomUser, id=user_id)

        if target_user == request.user:
            return redirect('profile')  # Can't follow yourself

        follow_relation, created = Follow.objects.get_or_create(
            follower=request.user,
            following=target_user
        )

        if not created:
            follow_relation.delete()

        return redirect('user_profile', username=target_user.username)

    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def profile(request):
    user = request.user
    profile = user.profile
    posts = Post.objects.filter(author=user)
    followers = Follow.objects.filter(following=user)
    following = Follow.objects.filter(follower=user)

    return render(request, 'users/profile.html', {
        'profile_user': user,
        'profile': profile,
        'posts': posts,
        'followers': followers,
        'following': following,
        'is_following': False,  # No follow button when viewing own profile
    })


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', {'form': form})


@login_required
def user_profile(request, username):
    profile_user = get_object_or_404(CustomUser, username=username)
    posts = Post.objects.filter(author=profile_user)
    followers = Follow.objects.filter(following=profile_user)
    following = Follow.objects.filter(follower=profile_user)
    
    is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()

    return render(request, 'users/profile.html', {
        'profile_user': profile_user,
        'posts': posts,
        'followers': followers,
        'following': following,
        'is_following': is_following,
    })

def home(request):
    posts = Post.objects.all().order_by('-created_at')

    for post in posts:
        post.liked_by_user = post.likes.filter(user=request.user).exists()

    context = {
        'posts': posts
    }
    return render(request, 'users/home.html', {'posts': posts})

# users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Post, Comment, Profile
from django.contrib.auth import get_user_model
from django.forms import DateInput
User = get_user_model()

# Registration form for CustomUser
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

# Form to update user profile
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name')

# Post creation form
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption', 'image']

# Comment form
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class ProfileForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'birthdate', 'profile_picture']
        widgets = {
            'birthdate': DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['email'].initial = user.email

class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
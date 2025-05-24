from django.contrib import admin
from .models import Profile

# ✅ Do NOT register User again if you're using Django's default User model
# from django.contrib.auth import get_user_model
# from django.contrib.auth.admin import UserAdmin
# User = get_user_model()
# admin.site.register(User, UserAdmin)  # ❌ REMOVE this

# ✅ Register the Profile model only
admin.site.register(Profile)

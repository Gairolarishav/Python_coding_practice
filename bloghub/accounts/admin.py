from django.contrib import admin
from .models import User,Profile
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class ProfileInline(admin.StackedInline):  # edit profile inside the user page
    model = Profile
    can_delete = False


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]
    list_display = ["username", "email", "is_staff"]

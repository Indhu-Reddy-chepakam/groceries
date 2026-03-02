from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Profile, ContactMessage

# -------------------------------
# Contact Message Admin
# -------------------------------
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'message', 'created_at')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('created_at',)

# -------------------------------
# Profile Inline for User
# -------------------------------
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

# -------------------------------
# Custom User Admin
# -------------------------------
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')

# Unregister default User
admin.site.unregister(User)

# Register User again with Profile inline
admin.site.register(User, CustomUserAdmin)

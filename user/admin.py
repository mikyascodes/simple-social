from django.contrib import admin
from .models import Notification, UserProfile, Message
from django.contrib.auth.models import User


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "bio", "avatar", "profile_status")


admin.site.register(UserProfile, UserProfileAdmin)


admin.site.unregister(User)


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")


admin.site.register(User, UserAdmin)


class MessageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Message, MessageAdmin)


class NotificationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Notification, NotificationAdmin)

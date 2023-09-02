from django.contrib import admin
from .models import UserProfile,FriendRequest,ChatMessage
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(FriendRequest)
admin.site.register(ChatMessage)
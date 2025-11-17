from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Post, Notification

admin.site.register(Post)

admin.site.register(Notification)
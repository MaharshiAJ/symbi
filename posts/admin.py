from django.contrib import admin

from .models import ActivityPost, Comment


@admin.register(ActivityPost)
class ActivityPostAdmin(admin.ModelAdmin):
    list_display = ["title", "description"]
    search_fields = ["title"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["content"]
    search_fields = ["content"]

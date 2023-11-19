from django.contrib import admin

from .models import ActivityPost


@admin.register(ActivityPost)
class ActivityPostAdmin(admin.ModelAdmin):
    list_display = ["title", "description"]
    search_fields = ["title"]

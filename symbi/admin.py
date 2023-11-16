from django.contrib import admin

from .models import InterestTag, SymbiUser


@admin.register(InterestTag)
class InterestTagAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(SymbiUser)
class SymbiUserAdmin(admin.ModelAdmin):
    list_display = [
        "username",
        "email",
        "full_name",
        "pronouns",
        "date_of_birth",
        "major",
    ]
    search_fields = ["username"]

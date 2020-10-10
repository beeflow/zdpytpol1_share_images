from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    def followers_count(self, instance: User):
        return instance.followers.count()

    def followed_count(self, instance: User):
        return instance.followed.count()

    followers_count.short_description = "followed by"
    followed_count.short_description = "follows"

    list_display = ("username", "is_superuser", "followers_count", "followed_count")

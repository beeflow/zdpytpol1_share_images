from django.contrib.auth import get_user_model
from rest_framework import serializers

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()
    followed = serializers.SerializerMethodField()

    class Meta:
        model = UserModel
        fields = ("id", "username", "first_name", "last_name", "followers", "followed")

    def get_followers(self, instance):
        return instance.followers.count()

    def get_followed(self, instance):
        return instance.followed.count()

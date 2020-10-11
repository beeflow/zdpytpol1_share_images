from rest_framework import serializers

from apiv1.serializers.userserializer import UserSerializer
from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    likes = serializers.SerializerMethodField()

    def get_likes(self, instance):
        return instance.liked_by.count()

    class Meta:
        model = Post
        fields = "__all__"
        depth = 1

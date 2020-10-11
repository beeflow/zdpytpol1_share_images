from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from apiv1.serializers.userserializer import RegisterUserSerializer, UserSerializer
from posts.models import Post

UserModel = get_user_model()


class CreateUserView(CreateAPIView):
    model = UserModel
    serializer_class = RegisterUserSerializer
    permission_classes = [permissions.AllowAny]


class UsersListView(ListAPIView):
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()


class FollowView(APIView):
    def get(self, request, username):
        try:
            user = (UserModel.objects.get(username=username),)
            request.user.follow(user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UserModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class UnfollowView(APIView):
    def get(self, request, username):
        try:
            user = UserModel.objects.get(username=username)
            request.user.unfollow(user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UserModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class AddPostView(APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request, filename=None):
        file = request.data["file"]
        post = Post.objects.create(image=file, owner=request.user)
        return Response({"id": str(post.id)}, status=status.HTTP_201_CREATED)

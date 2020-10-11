from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from apiv1.serializers.postserializer import PostSerializer
from apiv1.serializers.userserializer import RegisterUserSerializer, UserSerializer
from posts.models import Post
from users.models import Follower

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


class AddPostCaptionView(APIView):
    def put(self, request, pk):
        try:
            post = Post.objects.get(pk=pk, owner=request.user)
            post.caption = request.POST.get("caption")
            post.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValidationError as error:
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)


class LikePostView(APIView):
    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            post.like(request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValidationError as error:
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)


class UnlikePostView(APIView):
    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            post.unlike(request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValidationError as error:
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)


class PostsListView(ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by("likes")


class UserPostsListView(ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(owner=self.request.user).order_by("-created_at")


class UserFollowedPostListView(ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        user_followed = [followed.follow for followed in Follower.objects.filter(user=self.request.user)]
        return Post.objects.filter(owner__in=user_followed).order_by("-created_at")

        # 1. list uzytkownikow, ktorych sledzimy(obserwujemy)
        # users_followed = []
        # # 1a. lista obiektow z modelu follower, gdzie w atrybucie user znajduje sie zalogowany uzytkownik
        # for followed in Follower.objects.filter(user=self.request.user):
        #     ## 1b. z kazdego obiketu follower wybieramy uzytkownika z atrybutu follow
        #     users_followed.append(followed.follow)
        # ## 2. lista postow, ktorych wlasciciel znajduje sie na liscie obserwowanmych (z pkt 1)
        # return Post.objects.filter(owner__in=users_followed).order_by("-created_at")

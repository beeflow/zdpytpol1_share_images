from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, ListAPIView

from apiv1.serializers.userserializer import RegisterUserSerializer, UserSerializer


class CreateUserView(CreateAPIView):
    model = get_user_model()
    serializer_class = RegisterUserSerializer
    permission_classes = [permissions.AllowAny]


class UsersListView(ListAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

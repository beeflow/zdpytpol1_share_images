from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView

from apiv1.serializers.userserializer import UserSerializer


class UsersListView(ListAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

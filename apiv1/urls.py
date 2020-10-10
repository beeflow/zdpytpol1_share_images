from django.conf.urls import url
from django.urls import include, path

from . import views

app_name = "apiv1"

urlpatterns = [
    url(r'^auth/', include('djoser.urls.authtoken')),
    path("users/list", views.UsersListView.as_view(), name="users_list"),
]

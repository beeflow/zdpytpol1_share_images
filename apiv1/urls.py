from django.conf.urls import url
from django.urls import include, path

from . import views

app_name = "apiv1"

urlpatterns = [
    path("auth/register", views.CreateUserView.as_view(), name="users_create"),
    url(r"^auth/", include("djoser.urls.authtoken")),
    path("users/", views.UsersListView.as_view(), name="users_list"),
    path("users/follow/<username>", views.FollowView.as_view(), name="users_follow"),
    path("users/unfollow/<username>", views.UnfollowView.as_view(), name="users_unfollow"),
]

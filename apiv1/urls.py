from django.conf.urls import url
from django.urls import include, path, re_path

from . import views

app_name = "apiv1"

urlpatterns = [
    path("auth/register", views.CreateUserView.as_view(), name="users_register"),
    url(r"^auth/", include("djoser.urls.authtoken")),
    path("users/", views.UsersListView.as_view(), name="users_list"),
    path("users/follow/<username>", views.FollowView.as_view(), name="users_follow"),
    path("users/unfollow/<username>", views.UnfollowView.as_view(), name="users_unfollow"),
    re_path(r"^posts/upload_image/(?P<filename>[^/]+)$", views.AddPostView.as_view(), name="posts_add_image"),
    # path("posts/upload_image/<filename>", views.AddPostView.as_view(), name="posts_add_image"),
    path("posts/add_caption/<pk>", views.AddPostCaptionView.as_view(), name="posts_add_caption"),
    path("posts/like/<pk>", views.LikePostView.as_view(), name="posts_like"),
    path("posts/unlike/<pk>", views.UnlikePostView.as_view(), name="posts_unlike"),
    path("posts/all", views.PostsListView.as_view(), name="posts_all"),
    path("posts/", views.UserPostsListView.as_view(), name="posts_user"),
    path("posts/followed", views.UserFollowedPostListView.as_view(), name="posts_followed"),
]

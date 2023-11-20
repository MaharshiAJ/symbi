from django.urls import path
from . import views

app_name = "posts"
urlpatterns = [
    path("new/", views.CreatePostView.as_view(), name="create_post"),
    path(
        "post/<slug:poster>/<int:pk>/",
        views.PostDetailsView.as_view(),
        name="post_details",
    ),
    path(
        "post/edit/<slug:poster>/<int:pk>/",
        views.EditPostView.as_view(),
        name="edit_post",
    ),
    path(
        "post/<slug:post_poster>/<int:post_pk>/comment/<slug:comment_poster>/<int:comment_pk>/",
        views.DeleteCommentView.as_view(),
        name="delete_comment",
    ),
    path(
        "post/<slug:post_poster>/<int:post_pk>/comment/<slug:comment_poster>/<int:comment_pk>/",
        views.EditCommentView.as_view(),
        name="edit_comment",
    ),
]

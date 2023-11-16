from django.urls import path
from . import views

app_name = "posts"
urlpatterns = [
    path("new/", views.CreatePostView.as_view(), name="create_post"),
    path(
        "post/<slug:poster>/<slug:title>/",
        views.PostDetailsView.as_view(),
        name="post_details",
    ),
]

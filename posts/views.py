from django.shortcuts import render
from django.urls import reverse_lazy
import django.views.generic as generic

from .forms import NewPostForm
from .models import ActivityPost


class CreatePostView(generic.CreateView):
    model = ActivityPost
    template_name = "posts/create_post.html"
    form_class = NewPostForm

    def get_success_url(self):
        return reverse_lazy(
            "posts:post_details",
            kwargs={
                "poster": self.object.poster.username,
                "title": self.object.title,
            },
        )

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.poster = self.request.user

        action = self.request.POST.get("action")
        if action == "draft":
            self.object.status = ActivityPost.DRAFT
        elif action == "post":
            self.object.status = ActivityPost.PostStatus.PUBLISHED

        self.object.save()

        return super().form_valid(form)


class PostDetailsView(generic.DetailView):
    model = ActivityPost
    template_name = "posts/post_details.html"
    context_object_name = "post"
    slug_field = "title"
    slug_url_kwarg = "title"


class EditPostView(generic.UpdateView):
    model = ActivityPost
    template_name = "posts/edit_post.html"
    form_class = NewPostForm
    slug_field = "title"
    slug_url_kwarg = "title"

    def get_success_url(self):
        return reverse_lazy(
            "posts:post_details",
            kwargs={
                "poster": self.object.poster.username,
                "title": self.object.title,
            },
        )

    def post(request, *args, **kwargs):
        pass


class DeletePostView(generic.DeleteView):
    model = ActivityPost
    template_name = "posts/delete_post.html"
    slug_field = "title"
    slug_url_kwarg = "title"
    success_url = reverse_lazy("posts:home")

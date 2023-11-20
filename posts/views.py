from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
import django.views.generic as generic

from .forms import EditPostForm, NewPostForm
from .models import ActivityPost, Comment
from symbi.models import SymbiUser


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = Comment.objects.filter(post=self.object).order_by(
            "-timestamp"
        )
        return context

    def post(self, request, *args, **kwargs):
        new_comment = self.request.POST.get("new_comment")
        poster = SymbiUser(username=self.kwargs["poster"])
        post = ActivityPost(poster=poster, pk=self.kwargs["pk"])
        Comment.objects.create(poster=request.user, post=post, content=new_comment)
        return redirect(
            reverse_lazy(
                "posts:post_details",
                kwargs={
                    "poster": poster.username,
                    "pk": post.id,
                },
            )
        )


class EditPostView(generic.UpdateView):
    model = ActivityPost
    template_name = "posts/edit_post.html"
    form_class = EditPostForm

    def get_success_url(self):
        post = get_object_or_404(
            ActivityPost,
            poster__username=self.kwargs["poster"],
            pk=self.kwargs["pk"],
        )
        return reverse_lazy(
            "posts:post_details",
            kwargs={
                "poster": post.poster.username,
                "pk": post.id,
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = get_object_or_404(
            ActivityPost,
            poster__username=self.kwargs["poster"],
            pk=self.kwargs["pk"],
        )
        return context

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(
            ActivityPost,
            poster__username=self.kwargs["poster"],
            pk=self.kwargs["pk"],
        )
        post.title = request.POST.get("title")
        post.description = request.POST.get("description")
        post.tags.set(request.POST.getlist("tags"))
        post.save()
        return redirect(self.get_success_url())


class DeletePostView(generic.DeleteView):
    model = ActivityPost
    template_name = "posts/delete_post.html"
    slug_field = "title"
    slug_url_kwarg = "title"
    success_url = reverse_lazy("posts:home")


class DeleteCommentView(generic.View):
    def get(self, request, *args, **kwargs):
        post = ActivityPost(
            poster__username=self.kwargs["post_poster"], pk=self.kwargs["post_pk"]
        )
        comment = Comment.objects.get(
            poster__username=self.kwargs["comment_poster"], pk=self.kwargs["comment_pk"]
        )
        comment.delete()
        return redirect(
            reverse_lazy(
                "posts:post_details",
                kwargs={
                    "poster": post.poster.username,
                    "pk": post.id,
                },
            )
        )


class EditCommentView(generic.View):
    def post(self, request, *args, **kwargs):
        post = ActivityPost(
            poster__username=self.kwargs["post_poster"], pk=self.kwargs["post_pk"]
        )
        comment = Comment.objects.get(
            poster__username=self.kwargs["comment_poster"], pk=self.kwargs["comment_pk"]
        )
        edited_comment = request.POST.get("edited_comment")
        comment.content = edited_comment
        comment.save()
        return redirect(
            reverse_lazy(
                "posts:post_details",
                kwargs={
                    "poster": post.poster.username,
                    "pk": post.id,
                },
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["edit_comment"] = False
        return context

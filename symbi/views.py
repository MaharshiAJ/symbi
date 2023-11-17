from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
import django.views.generic as generic
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, SignupForm
from .models import SymbiUser
from posts.models import ActivityPost


class HomePageView(generic.TemplateView):
    template_name = "symbi/home.html"


class LandingPageView(generic.TemplateView):
    template_name = "symbi/landing.html"


class LoginView(LoginView):
    template_name = "symbi/login.html"
    authentication_form = LoginForm
    success_url = reverse_lazy("symbi:home")


class SignupView(generic.FormView):
    template_name = "symbi/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy("symbi:home")

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect(self.success_url)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")

            return render(request, "symbi/signup.html", {"form": form})


class HomePageView(generic.TemplateView):
    template_name = "symbi/home.html"


class ProfilePageView(generic.DetailView):
    model = SymbiUser
    template_name = "symbi/profile_page.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        return get_object_or_404(SymbiUser, username=self.kwargs["username"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_posts"] = ActivityPost.objects.filter(poster=self.object)
        context["active_posts"] = ActivityPost.objects.filter(
            poster=self.object, status=ActivityPost.PostStatus.PUBLISHED
        )
        context["drafted_posts"] = ActivityPost.objects.filter(
            poster=self.object, status=ActivityPost.PostStatus.DRAFT
        )
        context["archived_posts"] = ActivityPost.objects.filter(
            poster=self.object, status=ActivityPost.PostStatus.ARCHIVED
        )
        return context

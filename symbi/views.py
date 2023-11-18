from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
import django.views.generic as generic
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, SignupForm
from .models import Connection, SymbiUser
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
        context["active_posts"] = ActivityPost.objects.filter(
            poster=self.object, status=ActivityPost.PostStatus.PUBLISHED
        )
        context["drafted_posts"] = ActivityPost.objects.filter(
            poster=self.object, status=ActivityPost.PostStatus.DRAFT
        )
        context["archived_posts"] = ActivityPost.objects.filter(
            poster=self.object, status=ActivityPost.PostStatus.ARCHIVED
        )
        context["connection"] = Connection.get_connection(
            self.request.user, self.object
        )
        return context


class LogoutView(generic.RedirectView):
    url = reverse_lazy("symbi:landing")

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class RequestConnectionView(generic.View):
    def get(self, request, *args, **kwargs):
        requester = get_object_or_404(SymbiUser, username=self.request.user)
        receiver = get_object_or_404(SymbiUser, username=self.kwargs["receiver"])

        if not Connection.are_connected(user, receiver):
            Connection.objects.create(
                requester=requester,
                receiver=receiver,
                status=Connection.ConnectionStatus.REQUESTED,
            )

        return redirect(
            reverse_lazy("symbi:profile", kwargs={"username": receiver.username})
        )


class CancelConnectionView(generic.View):
    def get(self, request, *args, **kwargs):
        requester = get_object_or_404(SymbiUser, username=self.kwargs["requester"])
        receiver = get_object_or_404(SymbiUser, username=self.kwargs["receiver"])

        current_user = get_object_or_404(SymbiUser, username=self.request.user)

        # Handles redirect differently since requester and receiver can both cancel the connection
        if current_user == requester and Connection.are_connected(requester, receiver):
            Connection.objects.filter(requester=requester, receiver=receiver).delete()

            return redirect(
                reverse_lazy("symbi:profile", kwargs={"username": receiver.username})
            )
        elif current_user == receiver and Connection.are_connected(requester, receiver):
            Connection.objects.filter(requester=requester, receiver=receiver).delete()
            return redirect(reverse_lazy("symbi:home"))

        return redirect(reverse_lazy("symbi:home"))


class AcceptConnectionView(generic.View):
    def get(self, request, *args, **kwargs):
        requester = get_object_or_404(SymbiUser, username=self.kwargs["requester"])
        receiver = get_object_or_404(SymbiUser, username=self.kwargs["receiver"])

        if Connection.are_connected(requester, receiver):
            Connection.objects.filter(requester=requester, receiver=receiver).update(
                status=Connection.ConnectionStatus.CONNECTED
            )

        return redirect(
            reverse_lazy("symbi:connections", kwargs={"username": receiver.username})
        )


class ConnectionsPageView(generic.DetailView):
    model = SymbiUser
    template_name = "symbi/connections_page.html"

    def get_object(self, queryset=None):
        return get_object_or_404(SymbiUser, username=self.kwargs.get("username"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_user"] = self.request.user
        context["active_requests"] = Connection.get_pending_connections(
            self.request.user
        )
        context["active_connections"] = Connection.get_active_connections(
            self.request.user
        )
        return context

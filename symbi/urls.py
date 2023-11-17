from django.urls import path
from . import views

app_name = "symbi"
urlpatterns = [
    # path("", views.HomePageView.as_view(), name="home"),
    path("", views.LandingPageView.as_view(), name="landing"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("home/", views.HomePageView.as_view(), name="home"),
    path("profile/<slug:username>", views.ProfilePageView.as_view(), name="profile"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path(
        "connection/accept/<slug:username>",
        views.AcceptConnection.as_view(),
        name="accept_connection",
    ),
    path(
        "connection/request/<slug:username>",
        views.RequestConnection.as_view(),
        name="request_connection",
    ),
    path(
        "connection/cancel/<slug:username>",
        views.CancelConnection.as_view(),
        name="cancel_connection",
    ),
]

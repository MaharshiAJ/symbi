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
        "connection/accept/<slug:requester>/<slug:receiver>",
        views.AcceptConnectionView.as_view(),
        name="accept_connection",
    ),
    path(
        "connection/request/<slug:receiver>",
        views.RequestConnectionView.as_view(),
        name="request_connection",
    ),
    path(
        "connection/cancel/<slug:requester>/<slug:receiver>",
        views.CancelConnectionView.as_view(),
        name="cancel_connection",
    ),
    path(
        "connections/<slug:username>",
        views.ConnectionsPageView.as_view(),
        name="connections",
    ),
    path("discover/", views.DiscoverPageView.as_view(), name="discover"),
]

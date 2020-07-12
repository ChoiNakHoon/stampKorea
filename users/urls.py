from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("login/line", views.line_login, name="line-login"),
    path("login/line/callback/", views.line_callback, name="line-callback"),
    path("login/facebook", views.facebook_login, name="fb-login"),
    path("login/facebook/callback", views.facebook_callback, name="fb-callback"),
    path("logout/", views.log_out, name="logout"),
    path("singup/", views.SignupView.as_view(), name="signup"),
    path(
        "verify/<str:key>/", views.complete_verification, name="complete-verification"
    ),
    path("check-verify/<str:user>", views.check_verification, name="check-email",),
    path(
        "re-send-verify/<str:user>",
        views.resend_verification_email,
        name="resend-email",
    ),
]

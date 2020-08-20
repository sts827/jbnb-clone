from django.urls import path
from . import views

app_name = "users"
urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("login/github/", views.github_login, name="github-login"),
    path("login/github/callback/", views.github_callback, name="github-callback"),
    path("logout/", views.log_out, name="logout"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path(
        "verify/<str:key>/", views.complete_verification, name="complete-verification"
    ),
]

# path("verify/<str:key>")는 verify/(..)을 가져옴 (str타입)
# path("login/github/callback",(..))에서 callback이 된다면 해당 OAuth의 id값과 key값을 .env에 저장한다.

import os
import requests
from django.views import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import forms, models


class LoginView(FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    # def post(self, request):
    #     form = forms.LoginForm(request.POST)
    #     if form.is_valid():
    #         email = form.cleaned_data.get("email")
    #         password = form.cleaned_data.get("password")
    #         # clean_data는 모든필드를 정리해준 결과이며 return을 해주지 않으면 None
    #         user = authenticate(request, username=email, password=password)
    #         if user is not None:
    #             login(request, user)
    #             return redirect(reverse("core:home"))
    #     return render(request, "users/login.html", {"form": form})


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # to do: add success message
    except models.User.DoesNotExist:
        # to do: add error message
        pass
    return redirect(reverse("core:home"))


# github_login은 view에서 아무것도 render하지 않고 github로 redirect한다.
# Authorization callback URL? => "http://127.0.0.1:8000/users/login/github/callback"
# github이 user를 보내는곳(redirect) 단, accept시에만(verification이 됬을때..)
def github_login(request):
    client_id = os.environ.get("GH_ID")
    # redirect_uri는 Authorization callback URL와 동일해야한다.
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    # scope?는 user의 정보를 나타낼 수 있는 범위... 보안상 read:user일때만 사용
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


# views내 urls.py에도 path를 설정한다. github이 redirect를 하는 주소가 있어야 하기 때문
# callback URI에서 code와 access_token을 교환
def github_callback(request):
    try:
        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")
        code = request.GET.get("code", None)

        if code is not None:
            token_request = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            token_json = token_request.json()
            # error가 있다면
            error = token_json.get("error", None)
            if error is not None:
                raise GithubException()
            else:
                access_token = token_json.get("access_token")
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Accept": "application/json",
                        "Authorization": f"token {access_token}",
                    },
                )
                profile_json = profile_request.json()
                print("github의 profile_json:", profile_json)
                username = profile_json.get("login", None)
                print("github의 username:", username)
                if username is not None:
                    name = profile_json.get("name")
                    email = profile_json.get("email")
                    print("github의 email:", email)
                    bio = profile_json.get("bio")
                    try:
                        # user에서 email을 가져옴
                        user = models.User.objects.get(email=email)
                        print("email로 가져온 username:", user)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise GithubException()
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            email=email,
                            first_name=name,
                            username=email,
                            bio=bio,
                            login_method=models.User.LOGIN_GITHUB,
                            email_verified=True,
                        )
                        # users는 set_unusuable_password()가 있음 user가 시도하는 어떤pw도 안 먹힘.
                        user.set_unusable_password()
                        user.save()
                        # print("user:", user)
                    login(request, user)
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException("Can't get your profile")
        else:
            raise GithubException("Can't get code")
    except GithubException:
        # send error message
        return redirect(reverse("users:login"))


class GithubException(Exception):
    pass


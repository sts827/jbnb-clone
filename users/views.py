import os
import requests
from django.views import View
from django.utils import translation
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponse
from django.views.generic import FormView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from . import forms, models, mixins


class LoginView(mixins.LoggedOutOnlyView, FormView):

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

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("core:home")

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
    messages.info(request, f"See you later")
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(mixins.LoggedOutOnlyView, FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm  # SignUpForm -> UserCreationForm Or, ModelForm
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
class GithubException(Exception):
    pass


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
            error = token_json.get("error", None)
            if error is not None:
                raise GithubException("Can't get access token")
            else:
                access_token = token_json.get("access_token")
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                profile_json = profile_request.json()
                print("github계정이 있는 user:", profile_json)
                username = profile_json.get("login", None)
                print("github의 username(owner):", username)
                if username is not None:
                    name = profile_json.get("name")
                    email = profile_json.get("email")
                    bio = profile_json.get("bio")
                    try:
                        user = models.User.objects.get(email=email)
                        # login(request, user)
                        # return redirect(reverse("core:home"))
                        print("email로 가져온 user검색 :", user)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise GithubException(
                                f"Please log in with: {user.login_method}"
                            )
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            email=email,
                            first_name=name,
                            username=email,
                            bio=bio,
                            login_method=models.User.LOGIN_GITHUB,
                            email_verified=True,
                        )
                        user.set_unusable_password()
                        user.save()
                        # login(request, user)
                        # return redirect(reverse("core:home"))
                    login(request, user)
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException("Can't get your profile")
        else:
            raise GithubException("Can't get code")
    except GithubException as e:
        return redirect(reverse("users:login"))


def kakao_login(request):
    # 관리자 계정에서 polaris_3,myimmortal827 삭제 후 signup->login으로 진행해야 함
    client_id = os.environ.get("KAKAO_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        code = request.GET.get("code")
        client_id = os.environ.get("KAKAO_ID")
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        )
        # token_json을 print해서 error확인
        token_json = token_request.json()
        error = token_json.get("error", None)
        if error is not None:
            raise KakaoException("Auth_Code에러, 개발자에 문의 해주세요")
        access_token = token_json.get("access_token")
        # 사용자의 정보 요청 (post혹은 get)
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        profile_json = profile_request.json()
        # Kakao data_frame=> {'properties':{nickname},'kakao_account':{'profile':{'nickname','thumbnail','profile_image','email'}}}
        # print("카카오 User:", profile_json)
        kakao_account = profile_json.get("kakao_account")
        profile = kakao_account.get("profile")
        email = kakao_account.get("email", None)
        # print("카카오 User Email:", email)
        if email is None:
            raise KakaoException("해당 Email이 존재하지 않습니다.")
        # 카카오 사용자 properties("이름,이메일,프로필")을 가져옴
        nickname = profile.get("nickname")
        # profile이미지가 있다면 user필드에 Avatar 업뎃
        profile_image = profile.get("profile_image_url")
        try:
            user = models.User.objects.get(email=email)  # user,email을 통해 db에서 검색
            # user가 있다면 로그인 방법 체크
            if user.login_method != models.User.LOGIN_KAKAO:
                raise KakaoException(f"{user.login_method}로 로그인해주세요")
        except models.User.DoesNotExist:  # user생성
            user = models.User.objects.create(
                email=email,
                username=email,
                first_name=nickname,
                login_method=models.User.LOGIN_KAKAO,
                email_verified=True,
            )
            # profile이미지
            if profile_image is not None:
                photo_request = requests.get(profile_image, None)
                # photo_request => byte이미지를 contentfile에 담는다.
                user.avatar.save(
                    f"{nickname}-avatar", ContentFile(photo_request.content)
                )
            user.set_unusable_password()
            user.save()
        login(request, user)
        messages.success(request, f"환영합니다!! {user.first_name}님, 통영사랑 상품권 사용 가능지역입니다.")
        return redirect(reverse("core:home"))
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class UserProfileView(DetailView):
    """ User's Profile """

    # UserProfileView가 뷰에서 찾았던 User에 의해서 유저가 대체되는 경우 발생함

    # url이 이동할때마다 해당 유저의 id값이 바뀐다. -> profile기능 X
    model = models.User
    context_object_name = "user_obj"

    # user객체
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    # view의 context data 확장


class UpdateProfileView(SuccessMessageMixin, UpdateView):
    """ UpdateProfileView definition:
     폼->렌더링->필드초기화를 모두 해주는 UpdateView로 간단하게 update할수 있다. """

    model = models.User
    template_name = "users/update-profile.html"
    fields = (
        "email",
        "first_name",
        "last_name",
        "gender",
        "bio",
        "birthdate",
        "language",
        "currency",
    )
    success_message = "Profile Updated"

    # user가 수정하기를 원하는 객체를 반환.
    def get_object(self, queryset=None):
        return self.request.user

    # def form_valid(self, form):
    #     self.object.username = email
    #     self.object.save()
    #     return super().form_valid(form)

    # Form클래스를 이용해서 customize시키자.
    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["email"].widget.attrs = {"placeholder": "email"}
        form.fields["first_name"].widget.attrs = {"placeholder": "first_name"}
        form.fields["last_name"].widget.attrs = {"placeholder": "last_name"}
        form.fields["gender"].widget.attrs = {"placeholder": "gender"}
        form.fields["bio"].widget.attrs = {"placeholder": "bio"}
        form.fields["birthdate"].widget.attrs = {"placeholder": "birthdate"}
        form.fields["language"].widget.attrs = {"placeholder": "language"}
        form.fields["currency"].widget.attrs = {"placeholder": "currency"}

        return form


class UpdatePasswordView(
    mixins.LoggedInOnlyView,
    mixins.EmailLoginOnlyView,
    SuccessMessageMixin,
    PasswordChangeView,
):

    template_name = "users/update-password.html"
    success_message = "Password Updated"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget.attrs = {"placeholder": "Current Password"}
        form.fields["new_password1"].widget.attrs = {"placeholder": "New Password"}
        form.fields["new_password2"].widget.attrs = {
            "placeholder": "Confirm New Password"
        }
        return form

    def get_success_url(self):
        return self.request.user.get_absolute_url()


@login_required
def switch_hosting(request):
    try:
        del request.session["is_hosting"]
    except KeyError:
        request.session["is_hosting"] = True
    return redirect(reverse("core:home"))


def switch_language(request):
    lang = request.GET.get("lang", None)
    if lang is not None:
        request.session[translation.LANGUAGE_SESSION_KEY] = lang
    return HttpResponse(status=200)

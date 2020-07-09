import os
import uuid
import requests
from django.views.generic import FormView, DetailView, UpdateView, View
from django.shortcuts import redirect, reverse, render
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
from . import forms, models, mixnis


class LoginView(mixnis.LoggedOutOnlyView, FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        if user.email_verified is False:
            print("인증 해주세요")
            log_out(self.request)
            return redirect(reverse("users:check-email", kwargs={"user": email}))
        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            messages.warning(self.request, f"Hi {self.request.user.first_name}")
            return next_arg
        else:
            messages.success(
                self.request, f"Welcome back {self.request.user.first_name}"
            )
            return reverse("core:home")


def log_out(request):

    """ Log Out definition """
    messages.warning(request, f"See you later {request.user.first_name}")
    logout(request)
    return redirect(reverse("core:home"))


class SignupView(mixnis.LoggedOutOnlyView, FormView):

    """ Sign up View Definition"""

    template_name = "users/signup.html"
    form_class = forms.SignUpForm

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)

    def get_success_url(self):
        user = self.request.user.email
        return reverse("users:check-email", kwargs={"user": user})


# 인증 메일 재발송
def resend_verification_email(request, user):
    user = models.User.objects.get(username=user)
    user.verify_email()
    return redirect(reverse("users:check-email", kwargs={"user": user.username}))


# 인증 메일 체크페이지
def check_verification(request, user):
    user = user
    return render(request, "emails/check_email.html", context={"user": user})


# 보내진 인증 메일을 클릭 했을 때 회원 가입을 완료하는 함수
def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
    except models.User.DoesNotExist:
        pass

    return redirect(reverse("core:home"))


class LineException(Exception):
    pass


def line_login(self):
    client_id = os.environ.get("LINE_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/line/callback"
    state = uuid.uuid4().hex[:10]
    os.environ["LINE_STATE"] = state
    return redirect(
        f"https://access.line.me/oauth2/v2.1/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&state={state}&scope=profile%20openid%20email%20"
    )


def line_callback(request):
    try:
        # Line 에서 로그인 인증 된 이후 설정된 리다이렉트 url로 code 전송
        code = request.GET.get("code", None)

        client_id = os.environ.get("LINE_ID")
        client_secret = os.environ.get("LINE_SECRET")
        redirect_uri = "http://127.0.0.1:8000/users/login/line/callback"
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": client_id,
            "client_secret": client_secret,
        }
        if code is not None:
            # requests api를 이용해서 post
            api_result = requests.post(
                "https://api.line.me/oauth2/v2.1/token",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data=data,
            )
            token_json = api_result.json()
            print(token_json)
            error = token_json.get("error", None)
            if error is not None:
                raise LineException("Can't get authorization code.")
            id_token = token_json.get("id_token")
            data = {
                "id_token": id_token,
                "client_id": client_id,
            }
            user_request = requests.post(
                "https://api.line.me/oauth2/v2.1/verify", data=data,
            )
            profile_json = user_request.json()
            email = profile_json.get("email", None)
            if email is None:
                raise LineException("Please also give me your email")
            name = profile_json.get("name", None)
            profile_image = profile_json.get("picture", None)
            try:
                # user가 존재 하는지
                user = models.User.objects.get(email=email)
                if user.login_method != models.User.LOGIN_LINE:
                    # Line으로 로그인 하지 않았다면
                    raise LineException(f"Please log in with: {user.login_method}")
            except models.User.DoesNotExist:
                user = models.User.objects.create(
                    username=email,
                    email=email,
                    first_name=name,
                    login_method=models.User.LOGIN_LINE,
                    email_verified=True,
                )
                # 소셜로그인 경우 비밀번호 필요치 않음
                user.set_unusable_password
                user.save()
                if profile_image is not None:
                    # 이미지 있으면
                    photo_request = requests.get(profile_image)
                    user.avatar.save(
                        f"{name}-avatar.jpg", ContentFile(photo_request.content),
                    )
            messages.success(request, f"Welcome back {user.first_name}")
            login(request, user)
            return redirect(reverse("core:home"))
    except LineException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))

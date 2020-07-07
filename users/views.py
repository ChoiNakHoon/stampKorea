from django.views.generic import FormView, DetailView, UpdateView
from django.shortcuts import redirect, reverse, render
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
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
            return redirect(reverse("users:check"))
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
    success_url = reverse_lazy("users:check")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)


def check_verification(request):
    print("check")
    return render(request, "emails/check_email.html")


def complete_verification(request, key):
    print("여기 compelte_verfication")
    try:
        user = models.User.objects.get(email_secret=key)
        print(user)
        print(user.email_verified)
        print(user.email_secret)
        user.email_verified = True
        user.email_secret = ""
        user.save()
    except models.User.DoesNotExist:
        pass

    return redirect(reverse("core:home"))

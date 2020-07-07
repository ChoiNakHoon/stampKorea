from django.views.generic import FormView, DetailView, UpdateView
from django.shortcuts import redirect, reverse
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
    messages.warning(request, f"See you later {request.user.first_name}")
    logout(request)
    return redirect(reverse("core:home"))

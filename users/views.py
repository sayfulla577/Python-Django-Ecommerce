from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.views import LogoutView, LoginView

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"User is created Login Now: {username}")
            return redirect('login')
    else:
        form = UserRegisterForm()
    context = {
        "form": form,
        "title": "Register"
    }
    return render(request, "users/register.html", context)


class LoginPage(LoginView):
    template_name = "users/login.html"
    extra_context = {"title": "Login"}


class LogOutPage(LogoutView):
    template_name = "users/logout.html"
    extra_context = {"title": "Log Out"}

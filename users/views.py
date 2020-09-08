from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .forms import (
    ProfileUpdateForm,
    UserUpdateForm,
)
from .models import Profile
from web_app.models import Post
from django.views.generic import ListView
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache


# ------ 1 register variantui ------
# from .forms import UserRegisterForm

# Create your views here.
# ------ 1 register veikia (visiems 3 login variantams) ------
# def register(request):
#     if request.method == "POST":
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get("username")
#             messages.success(request, f"Paskyra sukurta vartotojui {username}!")
#             return redirect("login")
#     else:
#         form = UserRegisterForm()

#     context = {"form": form, "title": "Registracija"}
#     return render(request, "users/register.html", context)


# ------ 2 register veikia (tik 2 ir 3 login variantams) ------
from .forms import RegisterForm
from django.contrib.auth.models import User


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        # print(form.cleaned_data.get("username"))
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password1 = form.cleaned_data.get("password1")
            User.objects.create_user(username, email, password1)
            messages.success(
                request, f"Paskyra sukurta vartotojui {username}! Galite jungtis."
            )
            return redirect("login")
    else:
        form = RegisterForm()

    context = {"form": form, "title": "Registracija"}
    return render(request, "users/register.html", context)


# ----------- 1 login veikia -----------
# from .forms import MyLoginForm


# def CustomLogin(request):
#     if request.method == "POST":
#         form = MyLoginForm(request.POST)
#         email = request.POST["email"]
#         password = request.POST["password"]
#         if form.is_valid:
#             user = authenticate(request, username=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect("home")
#             else:
#                 return redirect("login")
#     else:
#         form = MyLoginForm()

#     return render(request, "users/login.html", {"form": form})


# ----------- 2 login veikia -----------
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm


class CustomLogin(LoginView):
    authentication_form = CustomAuthenticationForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["title"] = "Prisijungimas"
        return context


# ----------- 3 login veikia -------------
# from .forms import MyLoginForm
# from django.core.exceptions import ValidationError


# def login_page(request):
#     if request.method == "POST":
#         form = MyLoginForm(request.POST)
#         if form.is_valid():
#             # veikia su tokiais pavadinimais:
#             # username = form.cleaned_data.get("name")
#             # password = form.cleaned_data.get("psw")
#             username = form.cleaned_data.get("email")
#             password = form.cleaned_data.get("password")
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect("home")
#             else:
#                 error_message = "Įvesti neteisingi duomenys."
#     else:
#         error_message = ""
#         form = MyLoginForm()

#     context = {"form": form, "error": error_message}

#     return render(request, "users/login.html", context)


class SignOutView(LogoutView):
    template_name = "users/logout.html"

    # The view part of the view – the method that accepts a request
    # argument from URLs plus arguments, and returns a HTTP response.
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Jus turite būti prisijungęs.")
        return super().dispatch(request, *args, **kwargs)


# Function-based view:
# @login_required
# def profile_posts(request):
#     posts = Post.objects.filter(user__username="Max")
#     context = {"posts": posts, "title": "Profilis"}
#     return render(request, "users/profile.html", context)
# Class-based view:
class ProfilePostListView(ListView):
    model = Post  # same as queryset = Post.objects.all()
    template_name = "users/profile.html"
    context_object_name = "posts"
    paginate_by = 3
    # ordering = ["-date_posted"]  # latest to oldest

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Post.objects.filter(user=user).order_by("-date_posted")

    def get_context_data(self, *args, **kwargs):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        context = super().get_context_data(*args, **kwargs)
        context.update({"user": user})
        return context


@login_required
def ProfileUpdate(request, *args, **kwargs):
    if request.method == "POST":
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )  # instance: it has to know which instance of the user profile to update
        u_form = UserUpdateForm(
            request.POST, user=request.user
        )  # it has to know which user to update

        if p_form.is_valid() and u_form.is_valid():
            p_form.save()
            u_form.save()
            update_session_auth_hash(request, u_form.user)
            messages.success(request, f"{request.user.username} paskyra atnaujinta!")
            return redirect("profile", username=request.user)
    else:
        p_form = ProfileUpdateForm(
            instance=request.user.profile
        )  # show user's profile (picture) in the form
        u_form = UserUpdateForm(
            user=request.user
        )  # pass user as kwargs to the form (and kwargs.pop in the form in __init__ method)

    context = {"p_form": p_form, "u_form": u_form, "title": "Paskyros atnaujinimas"}

    return render(request, "users/profile-update.html", context)

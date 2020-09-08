"""mini_project_max URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("web_app.urls")),
    # ------ 1 register veikia ------
    path("register/", user_views.register, name="register"),
    # ----- 1 login veikia -----
    # path("login/", user_views.CustomLogin, name="login"),
    # ----- 2 login veikia -----
    path(
        "login/",
        user_views.CustomLogin.as_view(template_name="users/login.html"),
        name="login",
    ),
    # ----- 3 login veikia -----
    # path("login/", user_views.login_page, name="login"),
    path("logout/", user_views.SignOutView.as_view(), name="logout"),
    # path("profile/<str:username>", user_views.profile, name="profile"),  # function-based view
    path(
        "profile/<str:username>",
        user_views.ProfilePostListView.as_view(),
        name="profile",
    ),  # class-based view
    path(
        "profile/<str:username>/update", user_views.ProfileUpdate, name="profile-update"
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

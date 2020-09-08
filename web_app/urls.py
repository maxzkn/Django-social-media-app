from django.urls import path
from web_app import views as web_app_views

# from .views import PostListView

urlpatterns = [
    path("", web_app_views.PostListView.as_view(), name="home"),
    path("post/<int:pk>", web_app_views.PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/like", web_app_views.PostLike, name="post-like"),
    path(
        "post/<int:pk>/delete",
        web_app_views.PostDeleteView.as_view(),
        name="post-delete",
    ),
    path(
        "post/<int:pk>/update",
        web_app_views.PostUpdateView.as_view(),
        name="post-update",
    ),
    path("upload/", web_app_views.post_upload, name="post-upload"),
]

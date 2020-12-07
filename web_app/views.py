from .models import Post
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from .forms import (
    PostUploadForm,
    CommentForm,
    ChangeTitleForm,
)
from users.models import Profile, Comment, Like
from django.views.generic import (
    ListView,
    DetailView,
    DeleteView,
    UpdateView,
)
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import os
from django.conf import settings

# Create your views here.


class PostListView(ListView):
    model = Post
    template_name = "web_app/home.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]  # latest to oldest
    paginate_by = 9


class PostDetailView(DetailView):
    model = Post
    template_name = "web_app/post_detail.html"
    form_class = CommentForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        post = Post.objects.get(pk=self.kwargs["pk"])
        comments = Comment.objects.filter(post__pk=self.kwargs["pk"])
        context = {"comment_form": form, "comments": comments, "post": post}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs["pk"])
        comments = Comment.objects.filter(post__pk=self.kwargs["pk"])
        form = self.form_class(request.POST)
        context = {"comment_form": form, "comments": comments, "post": post}
        if form.is_valid():
            user = request.user
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.posted_by = user
            new_comment.save()
            return redirect("post-detail", self.kwargs["pk"])
        else:
            # perkrauti puslapį, bet gražinti POST formą su klaidą:
            return render(request, self.template_name, context)


@login_required
def PostLike(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user not in post.liked.all():
        post.liked.add(request.user)
    else:
        post.liked.remove(request.user)

    # čia duomenų bazei, sukurti like objektą arba atnaujinti egzistuojantį:
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    # kai vartotojas paspaudzia mygtuka:
    if not created:  # jeigu objektas egzistuoja (update'inti ji)
        if like.value == "Patinka":  # jeigu jo value DB lygus Patinka
            like.value = "Daugiau nepatinka"  # pakeisti i Daugiau nepatinka
        else:
            like.value = "Patinka"

    # tas pats:
    # try:
    #     like = Like.objects.get(user=request.user, post=post)
    #     if like.value == "Patinka":
    #         like.value = "Daugiau nepatinka"
    #     else:
    #         like.value = "Patinka"
    # except Like.DoesNotExit:
    #     like = Like(user=request.user, post=post)

    like.save()
    post.likes = post.liked.all().count()
    post.save()

    return redirect("post-detail", post.id)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "web_app/post_detail.html"

    # pk_url_kwarg = "pk"
    # model = Post

    # def get_success_url(self, **kwargs):
    #     user = self.object.user
    #     return reverse("profile", kwargs={"username": user.username})

    # def test_func(self):
    #     post = self.get_object()
    #     # check if the logged in user is the post creator:
    #     if request.user == post.user:
    #         return True
    #     return False

    # tas pats kas viršuje:
    def get_object(self, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs.get("pk"))
        return post

    def test_func(self):
        post = get_object_or_404(Post, pk=self.kwargs.get("pk"))
        # check if the logged in user is the post creator:
        if (self.request.user == post.user) or (self.request.user.is_superuser):
            return True
        return False  # 403 Forbidden

    def get_success_url(self, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs.get("pk"))
        user = post.user
        os.remove(os.path.join(settings.MEDIA_ROOT, f"{post.video}".replace('/', '\\')))
        # lazy version of the reverse URL resolver. Unlike the traditional reverse function,
        # reverse_lazy won't execute until the value is needed.
        # It is useful because it prevent 'Reverse Not Found' exceptions when working with
        # URLs that may not be immediately known.It’s prevent to occur error when URLConf is not loaded:
        return reverse_lazy("profile", kwargs={"username": user.username})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = "web_app/post_detail.html"
    form_class = ChangeTitleForm

    def get(self, request, *args, **kwargs):
        post = self.get_object()
        title_form = self.form_class
        comments = Comment.objects.filter(post__pk=self.kwargs["pk"])
        context = {"title_form": title_form, "comments": comments, "post": post}
        return render(request, self.template_name, context)

    def get_success_url(self, **kwargs):
        post = self.get_object()
        return reverse("post-detail", kwargs={"pk": post.id})

    def test_func(self):
        post = self.get_object()
        if (self.request.user == post.user) or (self.request.user.is_superuser):
            return True
        return False  # 403 Forbidden

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = self.form_class(request.POST)
        comments = Comment.objects.filter(post__pk=self.kwargs["pk"])
        context = {"title_form": form, "post": post, "comments": comments}
        if form.is_valid():
            new_title = form.cleaned_data.get("title")
            post.title = new_title
            post.save()
            return redirect("post-detail", self.kwargs["pk"])
        # errors:
        else:
            # perkrauti puslapį, bet gražinti POST formą su klaidą:
            return render(request, self.template_name, context)


@login_required
def post_upload(request):
    if request.method == "POST":
        form = PostUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # title = form.cleaned_data.get("title")
            # video = form.cleaned_data.get("video")
            # without user error: NOT NULL constraint failed: users_post.user_id:
            # You need to add the value of the user field in Post object.
            # For that, before saving the post, you can attach the user from request.user.
            # Using form.save(commit=False) will create a Post instance 'in memory', but not yet saved
            # in the Database, then add the user to that Post instance (add some changes before saving it)
            post = form.save(commit=False)
            post.user = request.user
            # post.title = title
            # post.video = video
            post.save()
            return redirect("profile", request.user.username)
    else:
        form = PostUploadForm()

    context = {"form": form, "title": "Įkelti video"}
    return render(request, "web_app/post_upload.html", context)
